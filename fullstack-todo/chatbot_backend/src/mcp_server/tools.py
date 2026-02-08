"""MCP tools definitions for todo operations."""

from typing import Dict, Any, List
from uuid import UUID


# Define the available tools for the LLM to use
def get_todo_tools() -> List[Dict[str, Any]]:
    """
    Get the list of available todo operation tools for the LLM.

    Returns:
        List of tool definitions that can be used by the LLM for function calling.
    """
    return [
        {
            "name": "create_task",
            "description": "Creates a new todo task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the task to create"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "Lists all todo tasks for the user, with optional filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter tasks by status ('all', 'completed', 'pending'). Defaults to 'all'",
                        "enum": ["all", "completed", "pending"],
                        "default": "all"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tasks to return. Defaults to 100",
                        "default": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Number of tasks to skip. Defaults to 0",
                        "default": 0
                    }
                }
            }
        },
        {
            "name": "get_task",
            "description": "Retrieves a specific todo task by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to retrieve"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Updates properties of an existing todo task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title for the task (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the task (optional)"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Deletes a specific todo task by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "set_task_complete",
            "description": "Sets the completion status of a specific todo task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to update"
                    },
                    "is_completed": {
                        "type": "boolean",
                        "description": "Whether the task is completed or not"
                    }
                },
                "required": ["task_id", "is_completed"]
            }
        }
    ]


# Tool name to display name mapping
TOOL_DISPLAY_NAMES = {
    "create_task": "Create Task",
    "list_tasks": "List Tasks",
    "get_task": "Get Task",
    "update_task": "Update Task",
    "delete_task": "Delete Task",
    "set_task_complete": "Set Task Complete"
}


# Validation functions for each tool
async def validate_create_task_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for create_task tool."""
    errors = {}

    if "title" not in arguments or not arguments["title"]:
        errors["title"] = "Title is required"

    if "description" in arguments and arguments["description"] is not None and not isinstance(arguments["description"], str):
        errors["description"] = "Description must be a string"

    return errors


async def validate_list_tasks_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for list_tasks tool."""
    errors = {}

    if "status" in arguments and arguments["status"] not in ["all", "completed", "pending"]:
        errors["status"] = "Status must be one of: all, completed, pending"

    if "limit" in arguments:
        try:
            limit = int(arguments["limit"])
            if limit <= 0:
                errors["limit"] = "Limit must be a positive integer"
        except (ValueError, TypeError):
            errors["limit"] = "Limit must be a valid integer"

    if "offset" in arguments:
        try:
            offset = int(arguments["offset"])
            if offset < 0:
                errors["offset"] = "Offset must be a non-negative integer"
        except (ValueError, TypeError):
            errors["offset"] = "Offset must be a valid integer"

    return errors


async def validate_get_task_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for get_task tool."""
    errors = {}

    if "task_id" not in arguments or not arguments["task_id"]:
        errors["task_id"] = "Task ID is required"
    else:
        try:
            UUID(arguments["task_id"])
        except ValueError:
            errors["task_id"] = "Task ID must be a valid UUID"

    return errors


async def validate_update_task_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for update_task tool."""
    errors = {}

    if "task_id" not in arguments or not arguments["task_id"]:
        errors["task_id"] = "Task ID is required"
    else:
        try:
            UUID(arguments["task_id"])
        except ValueError:
            errors["task_id"] = "Task ID must be a valid UUID"

    # At least one of title or description must be provided
    if "title" not in arguments and "description" not in arguments:
        errors["fields"] = "At least one of title or description must be provided"

    if "title" in arguments and arguments["title"] is not None and not isinstance(arguments["title"], str):
        errors["title"] = "Title must be a string"

    if "description" in arguments and arguments["description"] is not None and not isinstance(arguments["description"], str):
        errors["description"] = "Description must be a string"

    return errors


async def validate_delete_task_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for delete_task tool."""
    errors = {}

    if "task_id" not in arguments or not arguments["task_id"]:
        errors["task_id"] = "Task ID is required"
    else:
        try:
            UUID(arguments["task_id"])
        except ValueError:
            errors["task_id"] = "Task ID must be a valid UUID"

    return errors


async def validate_set_task_complete_args(arguments: Dict[str, Any]) -> Dict[str, str]:
    """Validate arguments for set_task_complete tool."""
    errors = {}

    if "task_id" not in arguments or not arguments["task_id"]:
        errors["task_id"] = "Task ID is required"
    else:
        try:
            UUID(arguments["task_id"])
        except ValueError:
            errors["task_id"] = "Task ID must be a valid UUID"

    if "is_completed" not in arguments:
        errors["is_completed"] = "is_completed is required"
    elif not isinstance(arguments["is_completed"], bool):
        errors["is_completed"] = "is_completed must be a boolean value"

    return errors


# Mapping of tool names to their validation functions
TOOL_VALIDATORS = {
    "create_task": validate_create_task_args,
    "list_tasks": validate_list_tasks_args,
    "get_task": validate_get_task_args,
    "update_task": validate_update_task_args,
    "delete_task": validate_delete_task_args,
    "set_task_complete": validate_set_task_complete_args
}


async def validate_tool_arguments(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate the arguments for a given tool.

    Args:
        tool_name: Name of the tool to validate
        arguments: Arguments to validate

    Returns:
        Dictionary of validation errors (empty if no errors)
    """
    if tool_name not in TOOL_VALIDATORS:
        return {"tool": f"Unknown tool: {tool_name}"}

    validator = TOOL_VALIDATORS[tool_name]
    return await validator(arguments)


def get_tool_description(tool_name: str) -> str:
    """
    Get the description of a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Description of the tool
    """
    for tool in get_todo_tools():
        if tool["name"] == tool_name:
            return tool["description"]

    return f"Tool {tool_name} not found"