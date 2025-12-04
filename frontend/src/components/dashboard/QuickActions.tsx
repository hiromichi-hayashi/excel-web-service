import { Upload, FileText, BookTemplate } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export function QuickActions() {
  const actions = [
    {
      icon: Upload,
      label: "新規アップロード",
      description: "Excelファイルをアップロード",
      to: "/files/upload",
      color: "bg-blue-500",
    },
    {
      icon: FileText,
      label: "ファイル管理",
      description: "アップロード済みファイル",
      to: "/files",
      color: "bg-green-500",
    },
    {
      icon: BookTemplate,
      label: "テンプレート",
      description: "テンプレートを使用",
      to: "/templates",
      color: "bg-purple-500",
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>クイックアクション</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {actions.map((action) => (
            <Button
              key={action.label}
              variant="outline"
              asChild
              className="h-auto p-4"
            >
              <Link to={action.to}>
                <div className="flex flex-col items-center text-center space-y-2">
                  <div className={`p-3 rounded-full ${action.color}`}>
                    <action.icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 dark:text-gray-100">
                      {action.label}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {action.description}
                    </p>
                  </div>
                </div>
              </Link>
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
