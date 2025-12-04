import { useEffect, useState } from "react"
import { FileText, FolderOpen, Database } from "lucide-react"
import { useAuth } from "@/contexts/AuthContext"
import { fileApi } from "@/services/fileApi"
import { StatsCard } from "@/components/dashboard/StatsCard"
import { RecentFiles } from "@/components/dashboard/RecentFiles"
import { QuickActions } from "@/components/dashboard/QuickActions"
import type { File } from "@/types/file"

export function DashboardPage() {
  const { user } = useAuth()
  const [files, setFiles] = useState<File[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await fileApi.list(1, 10)
        setFiles(response.items)
      } catch (error) {
        console.error("Failed to fetch files:", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchFiles()
  }, [])

  const totalSize = files.reduce((sum, file) => sum + file.file_size, 0)
  const totalRows = files.reduce((sum, file) => sum + (file.rows_count || 0), 0)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          ダッシュボード
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          ようこそ、{user?.username}さん
        </p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">読み込み中...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatsCard
              title="ファイル数"
              value={files.length}
              icon={FileText}
              description="アップロード済み"
            />
            <StatsCard
              title="合計データ行数"
              value={totalRows.toLocaleString()}
              icon={Database}
              description="全ファイルの合計"
            />
            <StatsCard
              title="使用容量"
              value={`${(totalSize / 1024 / 1024).toFixed(2)} MB`}
              icon={FolderOpen}
              description="ストレージ使用量"
            />
          </div>

          <QuickActions />

          <RecentFiles files={files} />
        </>
      )}
    </div>
  )
}
