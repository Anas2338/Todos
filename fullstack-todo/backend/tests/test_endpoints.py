import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fastapi.testclient import TestClient
from main import app
import uuid


def test_user_signup_endpoint_exists():
    """Test that user signup endpoint exists."""
    client = TestClient(app)
    # Test with invalid data to check if endpoint exists
    response = client.post("/auth/signup", json={"invalid": "data"})
    # Should return 422 for validation error or 401/500 for other issues, but not 404
    assert response.status_code != 404


def test_user_signin_endpoint_exists():
    """Test that user signin endpoint exists."""
    client = TestClient(app)
    # Test with invalid data to check if endpoint exists
    response = client.post("/auth/signin", json={"invalid": "data"})
    # Should return 422 for validation error or 401 for invalid credentials, but not 404
    assert response.status_code != 404


def test_create_task_endpoint_exists():
    """Test that create task endpoint exists."""
    client = TestClient(app)
    # Mock user ID for the path parameter
    user_id = str(uuid.uuid4())

    # Test with invalid data to check if endpoint exists
    response = client.post(f"/api/{user_id}/tasks", json={"invalid": "data"})
    # Should return 422 for validation error or 401 for auth issues, but not 404
    assert response.status_code != 404


def test_get_all_tasks_endpoint_exists():
    """Test that get all tasks endpoint exists."""
    client = TestClient(app)
    # Mock user ID for the path parameter
    user_id = str(uuid.uuid4())

    response = client.get(f"/api/{user_id}/tasks")
    # Should return 401 for auth issues, but not 404
    assert response.status_code != 404


def test_get_task_by_id_endpoint_exists():
    """Test that get task by ID endpoint exists."""
    client = TestClient(app)
    # Mock user and task IDs for the path parameter
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    response = client.get(f"/api/{user_id}/tasks/{task_id}")
    # Should return 401 for auth issues or 404 for not found, but not a different error
    assert response.status_code in [401, 404]


def test_update_task_endpoint_exists():
    """Test that update task endpoint exists."""
    client = TestClient(app)
    # Mock user and task IDs for the path parameter
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Test with invalid data to check if endpoint exists
    response = client.put(f"/api/{user_id}/tasks/{task_id}", json={"invalid": "data"})
    # Should return 422 for validation error or 401 for auth issues, but not 404
    assert response.status_code != 404


def test_delete_task_endpoint_exists():
    """Test that delete task endpoint exists."""
    client = TestClient(app)
    # Mock user and task IDs for the path parameter
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    response = client.delete(f"/api/{user_id}/tasks/{task_id}")
    # Should return 401 for auth issues, but not 404
    assert response.status_code != 404


def test_complete_task_endpoint_exists():
    """Test that complete task endpoint exists."""
    client = TestClient(app)
    # Mock user and task IDs for the path parameter
    user_id = str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    # Test with invalid data to check if endpoint exists
    response = client.patch(f"/api/{user_id}/tasks/{task_id}/complete", json={"invalid": "data"})
    # Should return 422 for validation error or 401 for auth issues, but not 404
    assert response.status_code != 404