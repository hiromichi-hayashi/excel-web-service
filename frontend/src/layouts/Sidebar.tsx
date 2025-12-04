import { NavLink } from "react-router-dom"
import { useAuth } from "@/contexts/AuthContext"
import { LayoutDashboard, FileText, FileSpreadsheet, LogOut, User } from "lucide-react"

export const Sidebar = () => {
  const { user, logout } = useAuth()

  const navItems = [
    {
      to: "/",
      icon: LayoutDashboard,
      label: "ダッシュボード",
    },
    {
      to: "/files",
      icon: FileText,
      label: "ファイル管理",
    },
    {
      to: "/templates",
      icon: FileSpreadsheet,
      label: "テンプレート",
    },
  ]

  return (
    <aside className="flex w-64 flex-col border-r border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
      {/* ロゴエリア */}
      <div className="flex h-16 items-center border-b border-gray-200 px-6 dark:border-gray-700">
        <FileSpreadsheet className="mr-2 h-6 w-6 text-blue-600" />
        <span className="text-lg font-bold text-gray-800 dark:text-gray-100">Excel Service</span>
      </div>

      {/* ナビゲーション */}
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-50 text-blue-700 dark:bg-blue-900 dark:text-blue-200"
                  : "text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-gray-700"
              }`
            }
          >
            <item.icon className="h-5 w-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* ユーザー情報 */}
      <div className="border-t border-gray-200 p-4 dark:border-gray-700">
        <div className="mb-3 flex items-center gap-3 rounded-lg bg-gray-50 px-4 py-3 dark:bg-gray-700">
          <User className="h-5 w-5 text-gray-600 dark:text-gray-400" />
          <div className="flex-1 overflow-hidden">
            <p className="truncate text-sm font-medium text-gray-800 dark:text-gray-200">
              {user?.username}
            </p>
            <p className="truncate text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
          </div>
        </div>

        <button
          onClick={logout}
          className="flex w-full items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-red-600 transition-colors hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
        >
          <LogOut className="h-5 w-5" />
          ログアウト
        </button>
      </div>
    </aside>
  )
}
