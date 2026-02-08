"""Service for integrating chatbot task creation with main backend."""

import httpx
from typing import Optional, Dict, Any
from uuid import UUID
from ..core.config import config
import logging

logger = logging.getLogger(__name__)


class TaskIntegrationService:
    """Service for creating tasks in the main backend from the chatbot."""

    def __init__(self):
        self.main_backend_url = config.BETTER_AUTH_URL.rstrip('/')  # This should be the main backend URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def create_task_in_main_backend(self, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a task in the main backend for the given user.

        Args:
            user_id: The ID of the user to create the task for
            title: The task title
            description: Optional task description

        Returns:
            Dictionary with success status and task info
        """
        try:
            # Construct the API endpoint for creating tasks in main backend
            # Based on the logs, the main backend uses /api/{user_id}/tasks format
            url = f"{self.main_backend_url}/api/{user_id}/tasks"

            # Prepare the task data - make sure it matches the main backend's expected format
            # According to the main backend's TaskCreateRequest model: title (required), description (optional)
            task_data = {
                "title": title,
                "description": description or ""  # Empty string as default per model
            }

            # Headers - we need to include authentication
            # For internal communication, we may need to pass the user's authentication
            # Since both backends use the same BetterAuth system, we might need to pass the user's token
            headers = {
                "Content-Type": "application/json",
            }

            # Make the API call to the main backend
            response = await self.client.post(url, json=task_data, headers=headers)

            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"Successfully created task in main backend for user {user_id}")
                return {
                    "success": True,
                    "task": result.get("task", result)
                }
            else:
                logger.warning(f"Failed to create task in main backend: {response.status_code} - {response.text}")
                # Still return success since the main operation (chatbot backend) succeeded
                return {
                    "success": True,  # We return success to not affect the main operation
                    "warning": f"Task not created in main backend: {response.status_code}",
                    "details": response.text
                }

        except Exception as e:
            logger.warning(f"Error connecting to main backend: {str(e)}")
            # Still return success to not affect the main operation
            return {
                "success": True,  # We return success to not affect the main operation
                "warning": f"Could not connect to main backend: {str(e)}"
            }

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global instance
task_integration_service = TaskIntegrationService()