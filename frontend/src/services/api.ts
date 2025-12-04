import type { User, RegisterRequest, TokenResponse } from "@/types/auth"

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
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
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
  async login(email: string, password: string): Promise<TokenResponse> {
    return this.request<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    })
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
