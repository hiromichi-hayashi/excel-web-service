import { useEffect, useState } from "react"
import { FileText, Download } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { templateApi } from "@/services/fileApi"
import type { Template } from "@/types/file"

export const TemplatesPage = () => {
  const navigate = useNavigate()
  const [templates, setTemplates] = useState<Template[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchTemplates = async () => {
      try {
        const response = await templateApi.list()
        setTemplates(response.items)
      } catch (error) {
        console.error("Failed to fetch templates:", error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchTemplates()
  }, [])

  const handleUseTemplate = async (templateId: number) => {
    try {
      const newFile = await templateApi.use(templateId)
      navigate(`/files/${newFile.id}`)
    } catch (error) {
      console.error("Failed to use template:", error)
      alert("テンプレートの使用に失敗しました")
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-lg font-bold text-gray-900 dark:text-gray-100">テンプレート</h1>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">読み込み中...</p>
        </div>
      ) : templates.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400">テンプレートがまだありません</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <Card key={template.id} className="flex flex-col">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <FileText className="h-8 w-8 text-primary" />
                  <Badge variant={template.is_public ? "default" : "secondary"}>
                    {template.is_public ? "公開" : "非公開"}
                  </Badge>
                </div>
                <CardTitle className="mt-4">{template.name}</CardTitle>
                <CardDescription>{template.description || "説明なし"}</CardDescription>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col justify-end">
                <div className="space-y-2">
                  <div className="text-sm text-muted-foreground">
                    形式: <Badge variant="outline">{template.file_type.toUpperCase()}</Badge>
                  </div>
                  <Button className="w-full" onClick={() => handleUseTemplate(template.id)}>
                    <Download className="mr-2 h-4 w-4" />
                    このテンプレートを使用
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
