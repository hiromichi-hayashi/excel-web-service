"""
API エンドポイントのテスト
"""


def test_read_root(client):
    """ルートエンドポイントのテスト"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"


def test_health_check(client):
    """ヘルスチェックのテスト"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_api_info(client):
    """API情報のテスト"""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert data["api_version"] == "v1"
    assert data["framework"] == "FastAPI"
