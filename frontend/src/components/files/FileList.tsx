import { formatDistanceToNow } from "date-fns"
import { ja } from "date-fns/locale"
import { Eye, Download, Trash2, MoreHorizontal } from "lucide-react"
import { Link } from "react-router-dom"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import type { File } from "@/types/file"

interface FileListProps {
  files: File[]
  onDelete?: (id: number) => void
  onDownload?: (id: number) => void
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes"
  const k = 1024
  const sizes = ["Bytes", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i]
}

function getStatusBadge(status: string) {
  switch (status) {
    case "uploaded":
      return <Badge variant="secondary">アップロード済み</Badge>
    case "processing":
      return <Badge variant="warning">処理中</Badge>
    case "ready":
      return <Badge variant="success">準備完了</Badge>
    case "error":
      return <Badge variant="destructive">エラー</Badge>
    default:
      return <Badge>{status}</Badge>
  }
}

export const FileList = ({ files, onDelete, onDownload }: FileListProps) => {
  if (!files || files.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">ファイルがまだアップロードされていません</p>
      </div>
    )
  }

  return (
    <div className="border rounded-lg overflow-hidden bg-white dark:bg-gray-800 border-gray-400 dark:border-gray-600">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ファイル名</TableHead>
            <TableHead>形式</TableHead>
            <TableHead>サイズ</TableHead>
            <TableHead>行数</TableHead>
            <TableHead>列数</TableHead>
            <TableHead>ステータス</TableHead>
            <TableHead>アップロード日時</TableHead>
            <TableHead className="text-right">操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {files.map((file) => (
            <TableRow key={file.id}>
              <TableCell className="font-medium">
                <Link to={`/files/${file.id}`} className="hover:underline text-primary">
                  {file.original_filename}
                </Link>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{file.file_type.toUpperCase()}</Badge>
              </TableCell>
              <TableCell>{formatFileSize(file.file_size)}</TableCell>
              <TableCell>{file.rows_count?.toLocaleString() || "-"}</TableCell>
              <TableCell>{file.columns_count?.toLocaleString() || "-"}</TableCell>
              <TableCell>{getStatusBadge(file.status)}</TableCell>
              <TableCell>
                {formatDistanceToNow(new Date(file.created_at), {
                  addSuffix: true,
                  locale: ja,
                })}
              </TableCell>
              <TableCell className="text-right">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem asChild>
                      <Link to={`/files/${file.id}`} className="flex items-center">
                        <Eye className="mr-2 h-4 w-4" />
                        表示
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => onDownload?.(file.id)}>
                      <Download className="mr-2 h-4 w-4" />
                      ダウンロード
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      onClick={() => onDelete?.(file.id)}
                      className="text-red-600 dark:text-red-400"
                    >
                      <Trash2 className="mr-2 h-4 w-4" />
                      削除
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
