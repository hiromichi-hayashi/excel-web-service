import React, { createContext, useContext, useState, useEffect } from "react"
import { apiClient } from "@/services/api"
import type { User, AuthContextType } from "@/types/auth"

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(apiClient.getToken())
  const [isLoading, setIsLoading] = useState(true)

  // 初期化時にトークンがあれば現在のユーザーを取得
  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const currentUser = await apiClient.getCurrentUser()
          setUser(currentUser)
        } catch (error) {
          // トークンが無効な場合はクリア
          console.error("Failed to get current user:", error)
          setToken(null)
          apiClient.setToken(null)
        }
      }
      setIsLoading(false)
    }

    initAuth()
  }, [token])

  const login = async (email: string, password: string) => {
    try {
      const response = await apiClient.login(email, password)
      const newToken = response.access_token

      apiClient.setToken(newToken)
      setToken(newToken)

      // ログイン後にユーザー情報を取得
      const currentUser = await apiClient.getCurrentUser()
      setUser(currentUser)
    } catch (error) {
      throw error
    }
  }

  const register = async (email: string, username: string, password: string) => {
    try {
      await apiClient.register({ email, username, password })

      // 登録後に自動ログイン
      await login(email, password)
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    apiClient.setToken(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        register,
        logout,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
