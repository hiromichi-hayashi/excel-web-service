import { ArrowLeft, Download, Trash2 } from "lucide-react"
import { Link, useParams, useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { SpreadsheetViewer } from "@/components/spreadsheet/SpreadsheetViewer"
import { useFileData } from "@/hooks/useFileData"
import { fileApi } from "@/services/fileApi"

export const FileViewPage = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const fileId = id ? parseInt(id, 10) : undefined
  const { file, data, isLoading, error } = useFileData(fileId)

  const handleDownload = async () => {
    if (!file) return

    try {
      const blob = await fileApi.download(file.id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = file.original_filename
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Failed to download file:", error)
      alert("ファイルのダウンロードに失敗しました")
    }
  }

  const handleDelete = async () => {
    if (!file) return
    if (!confirm("このファイルを削除しますか？")) return

    try {
      await fileApi.delete(file.id)
      navigate("/files")
    } catch (error) {
      console.error("Failed to delete file:", error)
      alert("ファイルの削除に失敗しました")
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">読み込み中...</p>
        </div>
      </div>
    )
  }

  if (error || !file || !data) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" asChild>
          <Link to="/files">
            <ArrowLeft className="mr-2 h-4 w-4" />
            ファイル一覧に戻る
          </Link>
        </Button>
        <div className="text-center py-12">
          <p className="text-red-500">ファイルの読み込みに失敗しました</p>
        </div>
      </div>
    )
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
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">
            {file.original_filename}
          </h1>
          <div className="flex gap-2">
            <Button variant="outline" onClick={handleDownload}>
              <Download className="mr-2 h-4 w-4" />
              ダウンロード
            </Button>
            <Button variant="destructive" onClick={handleDelete}>
              <Trash2 className="mr-2 h-4 w-4" />
              削除
            </Button>
          </div>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>ファイル情報</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm font-medium text-muted-foreground">ファイルサイズ</p>
              <p className="text-lg font-medium">{(file.file_size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">行数</p>
              <p className="text-lg font-medium">{file.rows_count?.toLocaleString() || "-"}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">列数</p>
              <p className="text-lg font-medium">{file.columns_count?.toLocaleString() || "-"}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">ステータス</p>
              <div className="mt-1">
                <Badge variant={file.status === "ready" ? "success" : "secondary"}>
                  {file.status}
                </Badge>
              </div>
            </div>
          </div>
          {file.description && (
            <div className="mt-4">
              <p className="text-sm font-medium text-muted-foreground">説明</p>
              <p className="text-sm">{file.description}</p>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>データプレビュー</CardTitle>
        </CardHeader>
        <CardContent>
          <SpreadsheetViewer data={data} />
        </CardContent>
      </Card>
    </div>
  )
}
