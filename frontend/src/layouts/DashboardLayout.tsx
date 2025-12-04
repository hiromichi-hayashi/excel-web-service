import { Outlet } from "react-router-dom"
import { Sidebar } from "@/layouts/Sidebar"

export function DashboardLayout() {
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* サイドバー */}
      <Sidebar />

      {/* メインコンテンツ */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* ヘッダー */}
        <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6 dark:border-gray-700 dark:bg-gray-800">
          <h1 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
            Excel Web Service
          </h1>
        </header>

        {/* コンテンツエリア */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
