import { useEffect, useState } from "react"
import { FileText, FileSpreadsheet } from "lucide-react"
import { fileApi } from "@/services/fileApi"
import { StatsCard } from "@/components/dashboard/StatsCard"
import { RecentFiles } from "@/components/dashboard/RecentFiles"
import { QuickActions } from "@/components/dashboard/QuickActions"
import type { File, Statistics } from "@/types/file"

export const DashboardPage = () => {
  const [files, setFiles] = useState<File[]>([])
  const [statistics, setStatistics] = useState<Statistics>({
    total_files: 0,
    total_templates: 0,
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 統計情報と最近のファイルを並行取得
        const [statsResponse, filesResponse] = await Promise.all([
          fileApi.getStatistics(),
          fileApi.list(1, 10),
        ])
        setStatistics(statsResponse)
        setFiles(filesResponse.items || [])
      } catch (error) {
        if (import.meta.env.MODE === "development") {
          console.error("Failed to fetch dashboard data:", error)
        }
        setFiles([])
        setStatistics({
          total_files: 0,
          total_templates: 0,
        })
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">ダッシュボード</h1>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">読み込み中...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <StatsCard
              title="ファイル数"
              value={statistics.total_files}
              icon={FileText}
              description="アップロード済み"
            />
            <StatsCard
              title="テンプレート数"
              value={statistics.total_templates}
              icon={FileSpreadsheet}
              description="利用可能"
            />
          </div>

          <QuickActions />

          <RecentFiles files={files} />
        </>
      )}
    </div>
  )
}
