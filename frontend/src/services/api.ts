import type { User, LoginRequest, RegisterRequest, TokenResponse } from "@/types/auth"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
    // ローカルストレージからトークンを復元
    this.token = localStorage.getItem("token")
  }

  setToken(token: string | null) {
    this.token = token
    if (token) {
      localStorage.setItem("token", token)
    } else {
      localStorage.removeItem("token")
    }
  }

  getToken(): string | null {
    return this.token
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    }

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: "An error occurred",
      }))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // 認証API
  async login(username: string, password: string): Promise<TokenResponse> {
    // OAuth2PasswordRequestFormの形式に合わせる
    const formData = new URLSearchParams()
    formData.append("username", username)
    formData.append("password", password)

    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: "ログインに失敗しました",
      }))
      throw new Error(error.detail || "ログインに失敗しました")
    }

    return response.json()
  }

  async register(data: RegisterRequest): Promise<User> {
    return this.request<User>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    })
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>("/api/auth/me")
  }

  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>("/health")
  }
}

export const apiClient = new ApiClient(API_BASE_URL)
