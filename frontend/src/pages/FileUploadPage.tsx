import { ArrowLeft } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { FileUpload } from "@/components/files/FileUpload"

export function FileUploadPage() {
  const navigate = useNavigate()

  const handleUploadSuccess = (fileId: number) => {
    navigate(`/files/${fileId}`)
  }

  const handleUploadError = (error: Error) => {
    console.error("Upload error:", error)
  }

  return (
    <div className="space-y-6">
      <div>
        <Button variant="ghost" asChild className="mb-4">
          <Link to="/files">
            <ArrowLeft className="mr-2 h-4 w-4" />
            ファイル一覧に戻る
          </Link>
        </Button>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          ファイルアップロード
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Excel/CSVファイルをアップロードして管理できます
        </p>
      </div>

      <div className="max-w-2xl">
        <FileUpload
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
        />
      </div>
    </div>
  )
}
