import { useEffect, useState } from "react"
import { Plus, ChevronLeft, ChevronRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { FileList } from "@/components/files/FileList"
import { fileApi } from "@/services/fileApi"
import type { File } from "@/types/file"

export function FilesPage() {
  const [files, setFiles] = useState<File[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const pageSize = 20

  const fetchFiles = async (pageNum: number) => {
    try {
      setIsLoading(true)
      const response = await fileApi.list(pageNum, pageSize)
      setFiles(response.items)
      setTotalPages(response.total_pages)
    } catch (error) {
      console.error("Failed to fetch files:", error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchFiles(page)
  }, [page])

  const handleDelete = async (id: number) => {
    if (!confirm("このファイルを削除しますか？")) return

    try {
      await fileApi.delete(id)
      await fetchFiles(page)
    } catch (error) {
      console.error("Failed to delete file:", error)
      alert("ファイルの削除に失敗しました")
    }
  }

  const handleDownload = async (id: number) => {
    try {
      const file = files.find((f) => f.id === id)
      if (!file) return

      const blob = await fileApi.download(id)
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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
            ファイル管理
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            アップロードしたファイルの一覧
          </p>
        </div>
        <Button asChild>
          <Link to="/files/upload">
            <Plus className="mr-2 h-4 w-4" />
            新規アップロード
          </Link>
        </Button>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">読み込み中...</p>
        </div>
      ) : (
        <>
          <FileList
            files={files}
            onDelete={handleDelete}
            onDownload={handleDownload}
          />

          {totalPages > 1 && (
            <div className="flex items-center justify-between">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                ページ {page} / {totalPages}
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                >
                  <ChevronLeft className="h-4 w-4 mr-1" />
                  前へ
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                >
                  次へ
                  <ChevronRight className="h-4 w-4 ml-1" />
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
