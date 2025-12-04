import { apiClient } from "./api"
import type {
  File,
  FileListResponse,
  FileDataResponse,
  FileUpdateData,
  Template,
  TemplateListResponse,
} from "@/types/file"

const API_BASE = "/api"

export const fileApi = {
  // ファイルアップロード
  async upload(file: globalThis.File): Promise<File> {
    const formData = new FormData()
    formData.append("file", file)

    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/upload`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: "アップロードに失敗しました",
      }))
      throw new Error(error.detail || `HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // ファイル一覧取得
  async list(page = 1, pageSize = 20): Promise<FileListResponse> {
    const token = apiClient.getToken()
    const response = await fetch(
      `${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files?page=${page}&page_size=${pageSize}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // ファイル詳細取得
  async get(id: number): Promise<File> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // ファイルデータ取得（グリッド表示用）
  async getData(id: number, maxRows?: number): Promise<FileDataResponse> {
    const token = apiClient.getToken()
    const url = maxRows
      ? `${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}/data?max_rows=${maxRows}`
      : `${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}/data`

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // ファイルダウンロード
  async download(id: number): Promise<Blob> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}/download`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.blob()
  },

  // ファイル削除
  async delete(id: number): Promise<void> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  },

  // ファイル情報更新
  async update(id: number, data: FileUpdateData): Promise<File> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/files/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },
}

export const templateApi = {
  // テンプレート一覧取得
  async list(): Promise<TemplateListResponse> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/templates`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // テンプレート詳細取得
  async get(id: number): Promise<Template> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/templates/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },

  // テンプレートから新規ファイル作成
  async use(id: number): Promise<File> {
    const token = apiClient.getToken()
    const response = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000"}${API_BASE}/templates/${id}/use`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  },
}
