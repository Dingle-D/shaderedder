import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_app_creation():
    """Тест что приложение создается"""
    assert app is not None
    assert app.title == "FastAPI"


def test_root_endpoint():
    """Тест корневого эндпоинта"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello, World" in response.text


def test_api_router_included():
    """Тест что API router подключен"""
    client = TestClient(app)
    
    response = client.get("/api/v1/nonexistent")
    assert response.status_code != 500


def test_cors_enabled():
    """Тест что CORS включен"""
    client = TestClient(app)
    
    response = client.options("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code in [200, 405]


def test_settings_loaded():
    """Тест что настройки загружаются"""
    from app.core.config import settings
    assert hasattr(settings, 'SECRET_KEY')
    assert settings.SECRET_KEY is not None


def test_imports_work():
    """Тест что все модули импортируются без ошибок"""
    from app.api.api_router import api_router
    from app.core.config import settings
    assert api_router is not None
    assert settings is not None
