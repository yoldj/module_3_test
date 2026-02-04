"""
Test cases for configuration
"""
import os
import pytest
from app.core.config import Settings


class TestSettings:
    """Test cases for Settings configuration"""

    def test_default_settings(self):
        """Test default settings values"""
        settings = Settings()

        assert settings.PROJECT_NAME == "Firewall Log Monitoring System"
        assert settings.VERSION == "1.0.0"
        assert settings.API_V1_PREFIX == "/api/v1"
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30

    def test_database_url_default(self):
        """Test default database URL"""
        settings = Settings()
        assert "sqlite:///" in settings.DATABASE_URL
        assert "firewall_logs.db" in settings.DATABASE_URL

    def test_cors_origins_default(self):
        """Test default CORS origins"""
        settings = Settings()
        assert "http://localhost:3000" in settings.CORS_ORIGINS
        assert isinstance(settings.CORS_ORIGINS, list)

    def test_environment_default(self):
        """Test default environment"""
        settings = Settings()
        assert settings.ENVIRONMENT in ["development", "production", "test"]

    def test_secret_key_exists(self):
        """Test that SECRET_KEY is set"""
        settings = Settings()
        assert settings.SECRET_KEY is not None
        assert len(settings.SECRET_KEY) > 0

    def test_database_echo_setting(self):
        """Test DATABASE_ECHO setting"""
        settings = Settings()
        assert isinstance(settings.DATABASE_ECHO, bool)
