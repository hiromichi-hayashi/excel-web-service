import { useAuth } from "@/contexts/AuthContext"
import { LoginForm } from "@/components/auth/LoginForm"
import { RegisterForm } from "@/components/auth/RegisterForm"
import { Dashboard } from "@/components/Dashboard"

function App() {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center space-y-2">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="text-muted-foreground">読み込み中...</p>
        </div>
      </div>
    )
  }

  if (user) {
    return <Dashboard />
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto max-w-4xl space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">Excel Web Service</h1>
          <p className="text-muted-foreground">
            FastAPI + React with JWT Authentication
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <LoginForm />
          <RegisterForm />
        </div>
      </div>
    </div>
  )
}

export default App
