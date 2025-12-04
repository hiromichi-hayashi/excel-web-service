import { useState, useEffect, useCallback } from "react"
import { fileApi } from "@/services/fileApi"
import type { File, FileDataResponse } from "@/types/file"

interface UseFileDataResult {
  file: File | null
  data: FileDataResponse | null
  isLoading: boolean
  error: Error | null
  refetch: () => Promise<void>
}

export const useFileData = (fileId: number | undefined, maxRows?: number): UseFileDataResult => {
  const [file, setFile] = useState<File | null>(null)
  const [data, setData] = useState<FileDataResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const fetchData = useCallback(async () => {
    if (!fileId) {
      setIsLoading(false)
      return
    }

    try {
      setIsLoading(true)
      setError(null)

      const [fileInfo, fileData] = await Promise.all([
        fileApi.get(fileId),
        fileApi.getData(fileId, maxRows),
      ])

      setFile(fileInfo)
      setData(fileData)
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch file data"))
    } finally {
      setIsLoading(false)
    }
  }, [fileId, maxRows])

  useEffect(() => {
    fetchData()
  }, [fetchData])

  return {
    file,
    data,
    isLoading,
    error,
    refetch: fetchData,
  }
}
