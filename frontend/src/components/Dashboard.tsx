import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { LogOut, User as UserIcon } from "lucide-react"

export const Dashboard = () => {
  const { user, logout } = useAuth()

  if (!user) return null

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto max-w-4xl space-y-8">
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-4xl font-bold tracking-tight">ダッシュボード</h1>
            <p className="text-muted-foreground">ようこそ、{user.username}さん</p>
          </div>
          <Button variant="outline" onClick={logout}>
            <LogOut className="mr-2 h-4 w-4" />
            ログアウト
          </Button>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <UserIcon className="h-5 w-5" />
              ユーザー情報
            </CardTitle>
            <CardDescription>現在ログイン中のユーザー情報</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">ユーザーID</p>
                <p className="text-lg font-medium">{user.id}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">ユーザー名</p>
                <p className="text-lg font-medium">{user.username}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">メールアドレス</p>
                <p className="text-lg font-medium">{user.email}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">登録日</p>
                <p className="text-lg font-medium">
                  {new Date(user.created_at).toLocaleDateString("ja-JP")}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Excel Web Service</CardTitle>
            <CardDescription>
              このダッシュボードでExcelファイル処理機能が利用できます
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">今後、ここにExcel処理機能が追加されます。</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
