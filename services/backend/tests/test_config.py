import pytest
from app.core.config import settings


class TestSettings:
    """Тесты конфигурации приложения"""
    
    def test_required_settings(self):
        """Тест обязательных настроек"""
        required_settings = [
            'SECRET_KEY',
            'API_V1_STR', 
        ]
        
        for setting in required_settings:
            assert hasattr(settings, setting), f"Missing required setting: {setting}"
            assert getattr(settings, setting) is not None, f"Setting {setting} is None"
    
    def test_secret_key_strength(self):
        """Тест силы SECRET_KEY"""
        assert len(settings.SECRET_KEY) >= 10
