import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

function App() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto max-w-4xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">Excel Web Service</h1>
          <p className="text-muted-foreground">
            FastAPI + React with shadcn/ui
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>ログイン</CardTitle>
              <CardDescription>アカウントにログインしてください</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">メールアドレス</Label>
                <Input id="email" type="email" placeholder="name@example.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">パスワード</Label>
                <Input id="password" type="password" />
              </div>
              <Button className="w-full">ログイン</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>新規登録</CardTitle>
              <CardDescription>新しいアカウントを作成</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">ユーザー名</Label>
                <Input id="username" placeholder="username" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new-email">メールアドレス</Label>
                <Input id="new-email" type="email" placeholder="name@example.com" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="new-password">パスワード</Label>
                <Input id="new-password" type="password" />
              </div>
              <Button variant="secondary" className="w-full">登録</Button>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>shadcn/ui コンポーネントサンプル</CardTitle>
            <CardDescription>
              Tailwind CSS ベースのUIコンポーネントライブラリ
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            <Button>Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App
