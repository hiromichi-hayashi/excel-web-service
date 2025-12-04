import { useMemo } from "react"
import { AgGridReact } from "@ag-grid-community/react"
import type { ColDef } from "@ag-grid-community/core"
import { ClientSideRowModelModule } from "@ag-grid-community/client-side-row-model"
import "@ag-grid-community/styles/ag-grid.css"
import "@ag-grid-community/styles/ag-theme-quartz.css"
import type { FileDataResponse } from "@/types/file"

interface SpreadsheetViewerProps {
  data: FileDataResponse
  height?: string
}

export function SpreadsheetViewer({ data, height = "600px" }: SpreadsheetViewerProps) {
  // 列定義を生成
  const columnDefs = useMemo<ColDef[]>(() => {
    return data.headers.map((header, index) => ({
      field: `col_${index}`,
      headerName: header,
      sortable: true,
      filter: true,
      resizable: true,
      minWidth: 100,
    }))
  }, [data.headers])

  // 行データを変換
  const rowData = useMemo(() => {
    return data.rows.map((row) => {
      const rowObj: Record<string, unknown> = {}
      row.forEach((value, index) => {
        rowObj[`col_${index}`] = value
      })
      return rowObj
    })
  }, [data.rows])

  const defaultColDef = useMemo<ColDef>(() => {
    return {
      flex: 1,
      minWidth: 100,
      editable: false,
    }
  }, [])

  return (
    <div className="w-full" style={{ height }}>
      <div className="ag-theme-quartz h-full">
        <AgGridReact
          modules={[ClientSideRowModelModule]}
          columnDefs={columnDefs}
          rowData={rowData}
          defaultColDef={defaultColDef}
          animateRows={true}
          pagination={true}
          paginationPageSize={100}
          paginationPageSizeSelector={[50, 100, 200, 500]}
          suppressCellFocus={true}
        />
      </div>
    </div>
  )
}
