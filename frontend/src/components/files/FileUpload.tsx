import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, File as FileIcon, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { fileApi } from "@/services/fileApi"
import { cn } from "@/lib/utils"

interface FileUploadProps {
  onUploadSuccess?: (fileId: number) => void
  onUploadError?: (error: Error) => void
}

export const FileUpload = ({ onUploadSuccess, onUploadError }: FileUploadProps) => {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0])
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
      "application/vnd.ms-excel": [".xls"],
      "text/csv": [".csv"],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    onDropRejected: (fileRejections) => {
      if (fileRejections.length === 0) return
      const rejection = fileRejections[0]
      if (rejection.errors.length === 0) return
      const errorCode = rejection.errors[0].code
      if (errorCode === "file-too-large") {
        setError("ファイルサイズは10MB以下にしてください")
      } else if (errorCode === "file-invalid-type") {
        setError("xlsx, xls, csv ファイルのみアップロード可能です")
      } else {
        setError("ファイルのアップロードに失敗しました")
      }
    },
  })

  const handleUpload = async () => {
    if (!selectedFile) return

    try {
      setUploading(true)
      setProgress(0)
      setError(null)

      // プログレスのシミュレーション
      const progressInterval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      const result = await fileApi.upload(selectedFile)

      clearInterval(progressInterval)
      setProgress(100)

      setTimeout(() => {
        setSelectedFile(null)
        setProgress(0)
        onUploadSuccess?.(result.id)
      }, 500)
    } catch (err) {
      const error = err instanceof Error ? err : new Error("アップロードに失敗しました")
      setError(error.message)
      onUploadError?.(error)
    } finally {
      setUploading(false)
    }
  }

  const handleRemove = () => {
    setSelectedFile(null)
    setError(null)
    setProgress(0)
  }

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-lg p-16 text-center cursor-pointer transition-colors min-h-[400px] flex flex-col items-center justify-center bg-white dark:bg-gray-800",
          isDragActive
            ? "border-primary bg-primary/10 dark:bg-primary/20"
            : "border-gray-400 dark:border-gray-600 hover:border-primary hover:bg-gray-100 dark:hover:bg-gray-700",
          uploading && "pointer-events-none opacity-50"
        )}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-600" />
        <p className="mt-6 text-lg font-medium text-gray-900 dark:text-gray-100">
          {isDragActive
            ? "ここにファイルをドロップ"
            : "クリックまたはドラッグ&ドロップでファイルをアップロード"}
        </p>
        <p className="mt-3 text-sm text-gray-500 dark:text-gray-400">
          xlsx, xls, csv ファイル（最大10MB）
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      {selectedFile && (
        <div className="border rounded-lg p-4 space-y-4 bg-white dark:bg-gray-800 border-gray-400 dark:border-gray-600">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileIcon className="h-5 w-5 text-primary" />
              <div>
                <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            {!uploading && (
              <Button variant="ghost" size="sm" onClick={handleRemove}>
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>

          {uploading && (
            <div className="space-y-2">
              <Progress value={progress} />
              <p className="text-xs text-center text-gray-500 dark:text-gray-400">
                アップロード中... {progress}%
              </p>
            </div>
          )}

          {!uploading && (
            <Button onClick={handleUpload} className="w-full">
              <Upload className="mr-2 h-4 w-4" />
              アップロード
            </Button>
          )}
        </div>
      )}
    </div>
  )
}
