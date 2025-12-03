import { useAuth } from "@/contexts/AuthContext"
import { AuthPage } from "@/components/auth/AuthPage"
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

  return <AuthPage />
}

export default App
