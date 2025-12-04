export interface File {
  id: number
  user_id: number
  filename: string
  original_filename: string
  file_type: string
  file_size: number
  file_path: string
  rows_count: number | null
  columns_count: number | null
  sheets_count: number | null
  status: string
  description: string | null
  created_at: string
  updated_at: string | null
  last_accessed_at: string | null
}

export interface FileListResponse {
  items: File[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface FileDataResponse {
  headers: string[]
  rows: unknown[][]
  total_rows: number
}

export interface Template {
  id: number
  name: string
  description: string | null
  file_type: string
  file_path: string
  thumbnail_path: string | null
  is_public: boolean
  created_by: number | null
  created_at: string
}

export interface TemplateListResponse {
  items: Template[]
  total: number
}

export interface FileUpdateData {
  description?: string
}

export interface Statistics {
  total_files: number
  total_templates: number
}
