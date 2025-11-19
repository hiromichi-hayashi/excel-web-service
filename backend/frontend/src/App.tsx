import { useState, useEffect } from 'react'
import './App.css'
import axios from 'axios'

interface ApiInfo {
  message?: string
  version?: string
  status?: string
  api_version?: string
  python_version?: string
  framework?: string
  database?: string
}

function App() {
  const [apiInfo, setApiInfo] = useState<ApiInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchApiInfo = async () => {
      try {
        const [rootResponse, infoResponse] = await Promise.all([
          axios.get('/api/v1/info'),
          axios.get('/'),
        ])
        setApiInfo({ ...rootResponse.data, ...infoResponse.data })
        setLoading(false)
      } catch (err) {
        setError('APIとの接続に失敗しました')
        setLoading(false)
        console.error(err)
      }
    }

    fetchApiInfo()
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>Excel Web Service</h1>
        <p>FastAPI + React でExcel処理を行うWebサービス</p>
      </header>

      <main className="app-main">
        {loading && <div className="loading">読み込み中...</div>}

        {error && <div className="error">{error}</div>}

        {apiInfo && !loading && (
          <div className="api-info">
            <h2>API情報</h2>
            <div className="info-grid">
              <div className="info-item">
                <span className="label">ステータス:</span>
                <span className="value status-ok">{apiInfo.status}</span>
              </div>
              <div className="info-item">
                <span className="label">バージョン:</span>
                <span className="value">{apiInfo.version}</span>
              </div>
              <div className="info-item">
                <span className="label">Python:</span>
                <span className="value">{apiInfo.python_version}</span>
              </div>
              <div className="info-item">
                <span className="label">フレームワーク:</span>
                <span className="value">{apiInfo.framework}</span>
              </div>
              <div className="info-item">
                <span className="label">データベース:</span>
                <span className="value">{apiInfo.database}</span>
              </div>
            </div>
          </div>
        )}

        <div className="features">
          <h2>機能（開発予定）</h2>
          <ul>
            <li>Excelファイルのアップロード</li>
            <li>データの表示・編集</li>
            <li>Excelファイルのダウンロード</li>
          </ul>
        </div>
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Excel Web Service</p>
      </footer>
    </div>
  )
}

export default App
