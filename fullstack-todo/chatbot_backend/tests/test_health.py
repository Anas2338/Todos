"""Health check tests for the AI Chatbot Backend."""

import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert data["version"] == "0.1.0"
    assert "checks" in data
    assert "database" in data["checks"]
    assert "external_services" in data["checks"]