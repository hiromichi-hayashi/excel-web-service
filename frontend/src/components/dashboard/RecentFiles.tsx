import { formatDistanceToNow } from "date-fns"
import { ja } from "date-fns/locale"
import { FileText, Eye } from "lucide-react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { File } from "@/types/file"

interface RecentFilesProps {
  files: File[]
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i]
}

export function RecentFiles({ files }: RecentFilesProps) {
  if (files.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            最近のファイル
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            まだファイルがありません
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="h-5 w-5" />
          最近のファイル
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {files.slice(0, 5).map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors"
            >
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <FileText className="h-5 w-5 text-primary flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {file.original_filename}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {formatFileSize(file.file_size)} •{" "}
                    {formatDistanceToNow(new Date(file.created_at), {
                      addSuffix: true,
                      locale: ja,
                    })}
                  </p>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                asChild
              >
                <Link to={`/files/${file.id}`}>
                  <Eye className="h-4 w-4" />
                </Link>
              </Button>
            </div>
          ))}
        </div>
        {files.length > 5 && (
          <div className="mt-4 text-center">
            <Button variant="link" asChild>
              <Link to="/files">すべて表示</Link>
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
