"""AI agent for orchestrating natural language todo management."""

from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime
from ..services.llm_client import gemini_client
from ..mcp_server.server import mcp_server
from ..mcp_server.tools import get_todo_tools, validate_tool_arguments
from ..services.chat_service import chat_service
from ..models.chat_message import MessageRole
import json
import re


class AIChatAgent:
    """AI agent that interprets natural language and selects appropriate MCP tools."""

    def __init__(self):
        """Initialize the AI agent."""
        self.llm_client = gemini_client
        self.mcp_server = mcp_server
        self.tools = get_todo_tools()

    async def process_message(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """
        Process a user message and return an AI-generated response.

        Args:
            session_id: The ID of the chat session
            user_message: The user's natural language message
            user_id: The ID of the authenticated user, or None for unauthenticated users

        Returns:
            AI-generated response to the user
        """
        # Get recent conversation history for context
        recent_messages = await chat_service.get_recent_messages(session_id, limit=10)

        # Format conversation history for the LLM
        conversation_context = []
        for msg in recent_messages:
            role = "user" if msg.role == MessageRole.USER else "assistant"
            conversation_context.append({
                "role": role,
                "content": msg.content
            })

        # Add the current user message
        conversation_context.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Check if the user is trying to perform an action that requires authentication
            # If user is not authenticated and trying to create/update/list tasks, inform them
            message_lower = user_message.lower().strip()

            # Check if this is an action that requires authentication
            requires_auth = any([
                any(pattern in message_lower for pattern in ["create", "add", "new", "task", "todo"]),
                any(pattern in message_lower for pattern in ["list", "show", "my", "all", "tasks", "todos"]),
                any(pattern in message_lower for pattern in ["update", "edit", "change", "modify"]),
                any(pattern in message_lower for pattern in ["delete", "remove", "cancel"]),
                any(pattern in message_lower for pattern in ["complete", "finish", "done"])
            ])

            if requires_auth and user_id is None:
                # Inform the user they need to authenticate for this action
                auth_required_msg = "To perform this action, you need to be logged in. Please sign in to create, view, or manage your tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # Check if the LLM should be used for general conversation
            # Only use tool-based approach for authenticated users or for simple queries
            tool_call_result = await self._determine_and_execute_tool(session_id, user_message, user_id)

            if tool_call_result:
                # If a tool was called successfully, return the tool result
                return tool_call_result
            else:
                # For unauthenticated users, we can still provide general AI responses
                # Prepare the tools for the LLM (only if user is authenticated)
                tools = self.tools if user_id is not None else []

                # Generate a response from the LLM
                response_data = await self.llm_client.chat_completions(
                    messages=conversation_context,
                    tools=tools
                )

                if not response_data["success"]:
                    # If LLM call failed, return an error message
                    error_msg = f"I'm sorry, I encountered an error: {response_data.get('error', 'Unknown error')}"

                    # Add the error message to the chat history
                    await chat_service.add_message(
                        session_id=session_id,
                        role=MessageRole.ASSISTANT,
                        content=error_msg
                    )

                    return error_msg

                # Process the LLM response
                llm_response = response_data["response"]

                # Add the assistant's message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=llm_response
                )

                return llm_response

        except Exception as e:
            # Handle any errors during processing
            error_msg = f"I'm sorry, I encountered an error processing your request: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg

    async def _determine_and_execute_tool(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> Optional[str]:
        """
        Determine if the user message requires a tool call and execute it if needed.

        Args:
            session_id: The ID of the chat session
            user_message: The user's natural language message

        Returns:
            Tool result if a tool was called, None otherwise
        """
        # Convert message to lowercase for easier matching
        message_lower = user_message.lower().strip()

        # Define all patterns first
        create_patterns = [
            r"create.*task",
            r"add.*task",
            r"make.*task",
            r"new.*task",
            r"create.*todo",
            r"add.*todo",
            r"new.*todo"
        ]

        list_patterns = [
            r"show.*task",
            r"list.*task",
            r"my.*task",
            r"all.*task",
            r"show.*todo",
            r"list.*todo",
            r"my.*todo",
            r"all.*todo",
            r"what.*task",
            r"what.*todo"
        ]

        update_patterns = [
            r"update.*task",
            r"change.*task",
            r"edit.*task",
            r"modify.*task",
            r"update.*todo",
            r"change.*todo",
            r"edit.*todo",
            r"modify.*todo"
        ]

        delete_patterns = [
            r"delete.*task",
            r"remove.*task",
            r"cancel.*task",
            r"delete.*todo",
            r"remove.*todo",
            r"cancel.*todo"
        ]

        complete_patterns = [
            r"complete.*task",
            r"finish.*task",
            r"done.*task",
            r"mark.*complete",
            r"mark.*done",
            r"complete.*todo",
            r"finish.*todo",
            r"done.*todo"
        ]

        # Check for create task intent
        for pattern in create_patterns:
            if re.search(pattern, message_lower):
                return await self._handle_create_task(session_id, user_message, user_id)

        # Additional check: if the message doesn't match other patterns and looks like a simple task,
        # treat it as a create task request
        # Check if it's not a list, update, delete, or complete command, but still looks like a task
        if (not any(re.search(pattern, message_lower) for pattern in list_patterns) and
            not any(re.search(pattern, message_lower) for pattern in update_patterns) and
            not any(re.search(pattern, message_lower) for pattern in delete_patterns) and
            not any(re.search(pattern, message_lower) for pattern in complete_patterns) and
            len(message_lower.split()) >= 1 and  # Has at least one word
            not any(word in message_lower for word in ["hello", "hi", "hey", "help", "thank", "thanks", "please", "yes", "no", "ok", "okay"])):  # Not a greeting or simple response
            return await self._handle_create_task(session_id, user_message, user_id)

        # Check for list tasks intent

        for pattern in list_patterns:
            if re.search(pattern, message_lower):
                return await self._handle_list_tasks(session_id, user_message, user_id)

        # Check for update task intent
        for pattern in update_patterns:
            if re.search(pattern, message_lower):
                return await self._handle_update_task(session_id, user_message, user_id)

        # Check for delete task intent
        for pattern in delete_patterns:
            if re.search(pattern, message_lower):
                return await self._handle_delete_task(session_id, user_message, user_id)

        # Check for set task complete intent
        for pattern in complete_patterns:
            if re.search(pattern, message_lower):
                return await self._handle_set_task_complete(session_id, user_message, user_id)

        # If no pattern matched, return None
        return None

    async def _handle_create_task(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """Handle create task intent."""
        try:
            # Check if user is authenticated
            if user_id is None:
                auth_required_msg = "To create tasks, you need to be logged in. Please sign in to create tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # Extract the task title from the user message
            # This is a simple approach - in practice, you'd want more sophisticated NLP
            import re

            # Look for patterns like "create task to buy groceries" or "add a task for homework"
            patterns = [
                r"create.*task.*to\s+(.+?)(?:\.|$)",
                r"add.*task.*to\s+(.+?)(?:\.|$)",
                r"create.*task.*for\s+(.+?)(?:\.|$)",
                r"add.*task.*for\s+(.+?)(?:\.|$)",
                r"create.*task\s+(.+?)(?:\.|$)",
                r"add.*task\s+(.+?)(?:\.|$)"
            ]

            title = None
            for pattern in patterns:
                match = re.search(pattern, user_message.lower())
                if match:
                    title = match.group(1).strip()
                    break

            # If we couldn't extract a title from the patterns, use the entire message
            # or a portion of it as the title
            if not title:
                # Remove common phrases and use the rest as title
                title = re.sub(r'(create|add|make|new)\s+(a\s+)?(task|todo)\s*', '', user_message, flags=re.IGNORECASE).strip()

                # If title is still empty or too short, ask for clarification
                if not title or len(title) < 2:
                    clarification_msg = "Could you please specify what task you'd like to create?"

                    # Add the clarification message to the chat history
                    await chat_service.add_message(
                        session_id=session_id,
                        role=MessageRole.ASSISTANT,
                        content=clarification_msg
                    )

                    return clarification_msg

            # Call the create_task tool
            arguments = {"title": title}
            result = await self.mcp_server.call_tool(session_id, "create_task", arguments)

            if result.get("success"):
                task = result["task"]
                response = f"I've created a task for you: '{task['title']}'."

                # Add the assistant's message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=response
                )

                return response
            else:
                error_msg = f"I'm sorry, I couldn't create the task: {result.get('error', {}).get('message', 'Unknown error')}"

                # Add the error message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=error_msg
                )

                return error_msg
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error creating the task: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg

    async def _handle_list_tasks(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """Handle list tasks intent."""
        try:
            # Check if user is authenticated
            if user_id is None:
                auth_required_msg = "To view your tasks, you need to be logged in. Please sign in to see your tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # Determine if user wants all, completed, or pending tasks
            status = "all"  # default
            if "completed" in user_message.lower():
                status = "completed"
            elif "pending" in user_message.lower() or "incomplete" in user_message.lower():
                status = "pending"

            # Call the list_tasks tool
            arguments = {"status": status}
            result = await mcp_server.call_tool(session_id, "list_tasks", arguments)

            if result.get("success"):
                tasks = result["tasks"]

                if not tasks:
                    if status == "completed":
                        response = "You don't have any completed tasks."
                    elif status == "pending":
                        response = "You don't have any pending tasks."
                    else:
                        response = "You don't have any tasks."
                else:
                    # Format the tasks into a response
                    task_list = []
                    for i, task in enumerate(tasks, 1):
                        status_text = "✓" if task["completed"] else "○"
                        task_list.append(f"{i}. {status_text} {task['title']}")

                    response = f"Here are your {status} tasks:\n" + "\n".join(task_list)

                # Add the assistant's message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=response
                )

                return response
            else:
                error_msg = f"I'm sorry, I couldn't retrieve your tasks: {result.get('error', {}).get('message', 'Unknown error')}"

                # Add the error message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=error_msg
                )

                return error_msg
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error listing your tasks: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg

    async def _handle_update_task(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """Handle update task intent."""
        try:
            # Check if user is authenticated
            if user_id is None:
                auth_required_msg = "To update tasks, you need to be logged in. Please sign in to update your tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # This is a more complex case that would require identifying which task to update
            # For simplicity, we'll ask for clarification
            clarification_msg = "To update a task, please specify which task you want to update and what changes to make. For example: 'Update task #1 to have title Buy Groceries'."

            # Add the clarification message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=clarification_msg
            )

            return clarification_msg
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error processing your update request: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg

    async def _handle_delete_task(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """Handle delete task intent."""
        try:
            # Check if user is authenticated
            if user_id is None:
                auth_required_msg = "To delete tasks, you need to be logged in. Please sign in to delete your tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # This is a complex case that would require identifying which task to delete
            # For simplicity, we'll ask for clarification
            clarification_msg = "To delete a task, please specify which task you want to delete. For example: 'Delete task #1' or 'Remove the grocery task'."

            # Add the clarification message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=clarification_msg
            )

            return clarification_msg
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error processing your delete request: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg

    async def _handle_set_task_complete(self, session_id: UUID, user_message: str, user_id: Optional[UUID] = None) -> str:
        """Handle set task complete intent."""
        try:
            # Check if user is authenticated
            if user_id is None:
                auth_required_msg = "To update task completion status, you need to be logged in. Please sign in to manage your tasks."

                # Add the message to the chat history
                await chat_service.add_message(
                    session_id=session_id,
                    role=MessageRole.ASSISTANT,
                    content=auth_required_msg
                )

                return auth_required_msg

            # Check if user wants to mark as complete or incomplete
            is_completed = "not" not in user_message.lower() and "incomplete" not in user_message.lower()

            # Extract task identifier (by number or title)
            import re

            # Try to extract task number from messages like "mark task #1 as complete" or "mark task 1 as complete"
            number_pattern = r"task\s+#?(\d+)"
            number_match = re.search(number_pattern, user_message.lower())

            if number_match:
                task_index = int(number_match.group(1)) - 1  # Convert to 0-based index

                # Get user's tasks to identify the specific task by index
                list_result = await self.mcp_server.call_tool(session_id, "list_tasks", {"status": "all"})

                if list_result.get("success"):
                    tasks = list_result["tasks"]

                    if 0 <= task_index < len(tasks):
                        target_task = tasks[task_index]
                        task_id = target_task["id"]

                        # Call the set_task_complete tool
                        arguments = {"task_id": task_id, "is_completed": is_completed}
                        result = await self.mcp_server.call_tool(session_id, "set_task_complete", arguments)

                        if result.get("success"):
                            action_word = "completed" if is_completed else "incomplete"
                            response = f"I've marked the task '{target_task['title']}' as {action_word}."

                            # Add the assistant's message to the chat history
                            await chat_service.add_message(
                                session_id=session_id,
                                role=MessageRole.ASSISTANT,
                                content=response
                            )

                            return response
                        else:
                            error_msg = f"I'm sorry, I couldn't update the task: {result.get('error', {}).get('message', 'Unknown error')}"

                            # Add the error message to the chat history
                            await chat_service.add_message(
                                session_id=session_id,
                                role=MessageRole.ASSISTANT,
                                content=error_msg
                            )

                            return error_msg
                    else:
                        error_msg = f"Task #{task_index + 1} doesn't exist. You have {len(tasks)} tasks."

                        # Add the error message to the chat history
                        await chat_service.add_message(
                            session_id=session_id,
                            role=MessageRole.ASSISTANT,
                            content=error_msg
                        )

                        return error_msg
                else:
                    error_msg = f"I couldn't retrieve your tasks to update the status: {list_result.get('error', {}).get('message', 'Unknown error')}"

                    # Add the error message to the chat history
                    await chat_service.add_message(
                        session_id=session_id,
                        role=MessageRole.ASSISTANT,
                        content=error_msg
                    )

                    return error_msg
            else:
                # Try to extract task by title (look for specific task name)
                # This is more complex, so for now we'll try to match by title if the user mentions it
                # Extract potential task title by looking for text after "mark" and before "as"
                title_pattern = r"mark\s+(.*?)\s+as"
                title_match = re.search(title_pattern, user_message.lower())

                if title_match:
                    potential_title = title_match.group(1).strip()

                    # Get user's tasks to find the one with matching title
                    list_result = await self.mcp_server.call_tool(session_id, "list_tasks", {"status": "all"})

                    if list_result.get("success"):
                        tasks = list_result["tasks"]

                        # Find task with matching title (case-insensitive partial match)
                        matching_task = None
                        for task in tasks:
                            if potential_title.lower() in task['title'].lower():
                                matching_task = task
                                break

                        if matching_task:
                            task_id = matching_task["id"]

                            # Call the set_task_complete tool
                            arguments = {"task_id": task_id, "is_completed": is_completed}
                            result = await self.mcp_server.call_tool(session_id, "set_task_complete", arguments)

                            if result.get("success"):
                                action_word = "completed" if is_completed else "incomplete"
                                response = f"I've marked the task '{matching_task['title']}' as {action_word}."

                                # Add the assistant's message to the chat history
                                await chat_service.add_message(
                                    session_id=session_id,
                                    role=MessageRole.ASSISTANT,
                                    content=response
                                )

                                return response
                            else:
                                error_msg = f"I'm sorry, I couldn't update the task: {result.get('error', {}).get('message', 'Unknown error')}"

                                # Add the error message to the chat history
                                await chat_service.add_message(
                                    session_id=session_id,
                                    role=MessageRole.ASSISTANT,
                                    content=error_msg
                                )

                                return error_msg
                        else:
                            error_msg = f"I couldn't find a task containing '{potential_title}'. Please specify the task number or check the task name."

                            # Add the error message to the chat history
                            await chat_service.add_message(
                                session_id=session_id,
                                role=MessageRole.ASSISTANT,
                                content=error_msg
                            )

                            return error_msg
                    else:
                        error_msg = f"I couldn't retrieve your tasks to update the status: {list_result.get('error', {}).get('message', 'Unknown error')}"

                        # Add the error message to the chat history
                        await chat_service.add_message(
                            session_id=session_id,
                            role=MessageRole.ASSISTANT,
                            content=error_msg
                        )

                        return error_msg
                else:
                    # If no task identifier found, ask for clarification
                    action_word = "complete" if is_completed else "incomplete"
                    clarification_msg = f"To mark a task as {action_word}, please specify which task. For example: 'Mark task #1 as {action_word}' or 'Mark the grocery task as {action_word}'."

                    # Add the clarification message to the chat history
                    await chat_service.add_message(
                        session_id=session_id,
                        role=MessageRole.ASSISTANT,
                        content=clarification_msg
                    )

                    return clarification_msg
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error processing your request: {str(e)}"

            # Add the error message to the chat history
            await chat_service.add_message(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=error_msg
            )

            return error_msg


# Global instance of the AI agent
ai_agent = AIChatAgent()