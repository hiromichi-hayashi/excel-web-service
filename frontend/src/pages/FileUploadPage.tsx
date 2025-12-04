import { ArrowLeft } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { FileUpload } from "@/components/files/FileUpload"

export const FileUploadPage = () => {
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
          <Link to="/files" className="flex items-center">
            <ArrowLeft className="mr-2 h-4 w-4" />
            ファイル一覧に戻る
          </Link>
        </Button>
        <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">ファイルアップロード</h1>
      </div>

      <FileUpload onUploadSuccess={handleUploadSuccess} onUploadError={handleUploadError} />
    </div>
  )
}
