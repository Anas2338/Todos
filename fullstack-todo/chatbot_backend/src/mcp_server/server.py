"""MCP server implementation for todo operations."""

from typing import Dict, Any, Optional
from uuid import UUID
import asyncio
from pydantic import BaseModel
from ..services.todo_service import todo_service
from ..models.tool_invocation import InvocationStatus
from ..services.chat_service import chat_service
from ..core.errors import MCPToolError, ValidationError


class MCPServer:
    """MCP Server implementation for handling todo operations."""

    def __init__(self):
        """Initialize the MCP server."""
        self.tools = {}
        self.register_default_tools()

    def register_tool(self, name: str, func):
        """Register a tool with the MCP server."""
        self.tools[name] = func

    def register_default_tools(self):
        """Register all default todo operation tools."""
        # Register all the required tools
        self.register_tool("create_task", self.handle_create_task)
        self.register_tool("list_tasks", self.handle_list_tasks)
        self.register_tool("get_task", self.handle_get_task)
        self.register_tool("update_task", self.handle_update_task)
        self.register_tool("delete_task", self.handle_delete_task)
        self.register_tool("set_task_complete", self.handle_set_task_complete)

    async def handle_create_task(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the create_task tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session or is not authenticated"
                    }
                }

            # Extract arguments
            title = arguments.get("title")
            description = arguments.get("description")

            if not title:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Title is required for creating a task"
                    }
                }

            # Call the todo service
            result = await todo_service.create_task(
                user_id=user_id,
                title=title,
                description=description
            )

            # Log the tool invocation - convert UUID to string for JSON serialization
            await chat_service.add_tool_invocation(
                session_id=str(session_id),  # Convert to string for JSON serialization
                tool_name="create_task",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if result.get("success") else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "CREATE_TASK_FAILED",
                    "message": f"Failed to create task: {str(e)}"
                }
            }

            # Log the failed tool invocation - convert UUID to string for JSON serialization
            await chat_service.add_tool_invocation(
                session_id=str(session_id),  # Convert to string for JSON serialization
                tool_name="create_task",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def handle_list_tasks(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the list_tasks tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session"
                    }
                }

            # Extract arguments with defaults
            status = arguments.get("status", "all")
            limit = arguments.get("limit", 100)
            offset = arguments.get("offset", 0)

            # Validate arguments
            if status not in ["all", "completed", "pending"]:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Status must be one of: all, completed, pending"
                    }
                }

            # Call the todo service
            result = await todo_service.list_tasks(
                user_id=user_id,
                status=status,
                limit=limit,
                offset=offset
            )

            # Log the tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="list_tasks",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if result.get("success") else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "LIST_TASKS_FAILED",
                    "message": f"Failed to list tasks: {str(e)}"
                }
            }

            # Log the failed tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="list_tasks",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def handle_get_task(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the get_task tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session"
                    }
                }

            # Extract arguments
            task_id_str = arguments.get("task_id")

            if not task_id_str:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "task_id is required for getting a task"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Invalid task_id format"
                    }
                }

            # Call the todo service
            result = await todo_service.get_task(
                user_id=user_id,
                task_id=task_id
            )

            # Log the tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="get_task",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if result.get("success") else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "GET_TASK_FAILED",
                    "message": f"Failed to get task: {str(e)}"
                }
            }

            # Log the failed tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="get_task",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def handle_update_task(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the update_task tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session"
                    }
                }

            # Extract arguments
            task_id_str = arguments.get("task_id")
            title = arguments.get("title")
            description = arguments.get("description")

            if not task_id_str:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "task_id is required for updating a task"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Invalid task_id format"
                    }
                }

            # At least one field should be provided for update
            if title is None and description is None:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "At least one of title or description must be provided for update"
                    }
                }

            # Call the todo service
            result = await todo_service.update_task(
                user_id=user_id,
                task_id=task_id,
                title=title,
                description=description
            )

            # Log the tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="update_task",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if result.get("success") else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "UPDATE_TASK_FAILED",
                    "message": f"Failed to update task: {str(e)}"
                }
            }

            # Log the failed tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="update_task",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def handle_delete_task(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the delete_task tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session"
                    }
                }

            # Extract arguments
            task_id_str = arguments.get("task_id")

            if not task_id_str:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "task_id is required for deleting a task"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Invalid task_id format"
                    }
                }

            # Call the todo service
            success = await todo_service.delete_task(
                user_id=user_id,
                task_id=task_id
            )

            result = {
                "success": success,
                "deleted_task_id": str(task_id) if success else None
            }

            # Log the tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="delete_task",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if success else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "DELETE_TASK_FAILED",
                    "message": f"Failed to delete task: {str(e)}"
                }
            }

            # Log the failed tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="delete_task",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def handle_set_task_complete(self, session_id: UUID, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the set_task_complete tool call."""
        try:
            # Get the user ID from the session
            user_id = await self._get_user_id_from_session(session_id)

            # Validate that the user owns the session
            owns_session = await self.validate_user_owns_session(user_id, session_id)
            if not owns_session:
                return {
                    "success": False,
                    "error": {
                        "code": "AUTHORIZATION_FAILED",
                        "message": "User does not own the session"
                    }
                }

            # Extract arguments
            task_id_str = arguments.get("task_id")
            is_completed = arguments.get("is_completed")

            if task_id_str is None:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "task_id is required for setting task completion"
                    }
                }

            if is_completed is None:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "is_completed is required for setting task completion"
                    }
                }

            if not isinstance(is_completed, bool):
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "is_completed must be a boolean value"
                    }
                }

            try:
                task_id = UUID(task_id_str)
            except ValueError:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Invalid task_id format"
                    }
                }

            # Call the todo service
            result = await todo_service.set_task_complete(
                user_id=user_id,
                task_id=task_id,
                is_completed=is_completed  # Keep the parameter name as is_completed since the function signature hasn't changed
            )

            # Log the tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="set_task_complete",
                arguments=arguments,
                result=result,
                status=InvocationStatus.SUCCESS if result.get("success") else InvocationStatus.ERROR
            )

            return result
        except Exception as e:
            error_result = {
                "success": False,
                "error": {
                    "code": "SET_TASK_COMPLETE_FAILED",
                    "message": f"Failed to set task completion: {str(e)}"
                }
            }

            # Log the failed tool invocation
            await chat_service.add_tool_invocation(
                session_id=str(session_id),
                tool_name="set_task_complete",
                arguments=arguments,
                result=error_result,
                status=InvocationStatus.ERROR
            )

            return error_result

    async def _get_user_id_from_session(self, session_id: UUID) -> Optional[UUID]:
        """
        Helper method to get user_id from session_id.
        In a real implementation, this would look up the session in the database.
        Returns None for anonymous sessions.
        """
        # This is a placeholder implementation
        # In a real system, we would fetch the session from the database
        # and return the associated user_id
        from ..models.chat_session import ChatSession
        from ..core.database import get_session_context
        from sqlmodel import select

        # Fetch the session from the database to get the user_id
        with get_session_context() as session:
            statement = select(ChatSession).where(ChatSession.id == session_id)
            db_session = session.exec(statement).first()

            if not db_session:
                raise ValueError(f"Session {session_id} not found")

            # Return None for anonymous sessions (where user_id is None)
            if db_session.user_id is None:
                return None

            # Ensure the returned user_id is a proper UUID object
            return UUID(str(db_session.user_id)) if isinstance(db_session.user_id, str) else db_session.user_id

    async def validate_user_owns_session(self, user_id: Optional[UUID], session_id: UUID) -> bool:
        """
        Validate that a user owns a specific session.
        For anonymous sessions (user_id is None), always return False to prevent tool usage.
        """
        if user_id is None:
            # Anonymous sessions cannot own tasks, so return False
            return False

        from ..services.chat_service import chat_service
        return await chat_service.validate_user_owns_session(user_id, session_id)

    async def call_tool(self, session_id: UUID, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a registered tool with the given arguments."""
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": f"Tool '{tool_name}' not found"
                }
            }

        # Call the tool function
        tool_func = self.tools[tool_name]
        return await tool_func(session_id, arguments)


# Global instance of the MCP server
mcp_server = MCPServer()