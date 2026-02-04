"""
Test cases for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestRootEndpoints:
    """Test cases for root API endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["message"] == "Firewall Log Monitoring API"
        assert data["docs"] == "/docs"

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "environment" in data
        assert data["status"] == "ok"

    def test_docs_endpoint_accessible(self):
        """Test that API docs are accessible"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint_accessible(self):
        """Test that ReDoc is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
