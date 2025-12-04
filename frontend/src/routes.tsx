import type { RouteObject } from "react-router-dom"
import { DashboardLayout } from "@/layouts/DashboardLayout"
import { DashboardPage } from "@/pages/DashboardPage"
import { FilesPage } from "@/pages/FilesPage"
import { FileUploadPage } from "@/pages/FileUploadPage"
import { FileViewPage } from "@/pages/FileViewPage"
import { TemplatesPage } from "@/pages/TemplatesPage"

export const routes: RouteObject[] = [
  {
    path: "/",
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "files",
        element: <FilesPage />,
      },
      {
        path: "files/upload",
        element: <FileUploadPage />,
      },
      {
        path: "files/:id",
        element: <FileViewPage />,
      },
      {
        path: "templates",
        element: <TemplatesPage />,
      },
    ],
  },
]
