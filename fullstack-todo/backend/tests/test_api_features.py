import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from main import app


def test_api_documentation():
    """Test that API documentation is accessible."""
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "docs" in response.text.lower()


def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
    assert "/auth/signup" in data["paths"]
    assert "/auth/signin" in data["paths"]
    assert "/api/{user_id}/tasks" in data["paths"]


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    client = TestClient(app)
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


if __name__ == "__main__":
    # This allows running the test directly with Python
    test_api_documentation()
    test_openapi_schema()
    test_invalid_endpoint()
    print("All tests passed!")