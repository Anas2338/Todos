"""Service for handling chat session management and message persistence."""

import json
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from datetime import datetime
from ..models.chat_session import ChatSession, ChatSessionCreate
from ..models.chat_message import ChatMessage, ChatMessageCreate, MessageRole
from ..models.tool_invocation import ToolInvocation, ToolInvocationCreate, InvocationStatus
from ..core.database import get_session_context


class ChatService:
    """Service for managing chat sessions and messages."""

    def __init__(self):
        pass

    async def create_session(self, user_id: UUID) -> UUID:
        """Create a new chat session for the user and return its ID."""
        with get_session_context() as session:
            # Create a new session
            db_session = ChatSession(
                user_id=user_id,
                title="New Chat",
                is_active=True
            )
            session.add(db_session)
            session.commit()
            session.refresh(db_session)

            # Return the ID directly to avoid detached session issues
            return db_session.id

    async def create_anonymous_session(self) -> UUID:
        """Create a new anonymous chat session and return its ID."""
        with get_session_context() as session:
            # Create a new session with no user_id (anonymous session)
            db_session = ChatSession(
                user_id=None,  # No user associated
                title="Anonymous Chat",
                is_active=True
            )
            session.add(db_session)
            session.commit()
            session.refresh(db_session)

            # Return the ID directly to avoid detached session issues
            return db_session.id

    async def get_session(self, session_id: UUID) -> Optional[ChatSession]:
        """Get a chat session by its ID."""
        with get_session_context() as session:
            statement = select(ChatSession).where(ChatSession.id == session_id)
            result = session.exec(statement).first()

            if result:
                # Force loading of attributes while session is still active
                session_id = result.id
                session_title = result.title
                session_user_id = result.user_id
                session_is_active = result.is_active
                session_created_at = result.created_at
                session_updated_at = result.updated_at

                # Create a new object with loaded values
                new_session = ChatSession(
                    id=session_id,
                    user_id=session_user_id,
                    title=session_title,
                    is_active=session_is_active
                )
                new_session.created_at = session_created_at
                new_session.updated_at = session_updated_at
                return new_session

            return None

    async def get_session_for_user(self, session_id: UUID, user_id: UUID) -> Optional[ChatSession]:
        """Get a chat session by its ID for a specific user (enforcing ownership)."""
        with get_session_context() as session:
            statement = select(ChatSession).where(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id
            )
            result = session.exec(statement).first()

            if result:
                # Force loading of attributes while session is still active
                session_id = result.id
                session_title = result.title
                session_user_id = result.user_id
                session_is_active = result.is_active
                session_created_at = result.created_at
                session_updated_at = result.updated_at

                # Create a new object with loaded values
                new_session = ChatSession(
                    id=session_id,
                    user_id=session_user_id,
                    title=session_title,
                    is_active=session_is_active
                )
                new_session.created_at = session_created_at
                new_session.updated_at = session_updated_at
                return new_session

            return None

    async def get_sessions_for_user(self, user_id: UUID) -> List[ChatSession]:
        """Get all chat sessions for a specific user."""
        with get_session_context() as session:
            statement = select(ChatSession).where(ChatSession.user_id == user_id)
            result = session.exec(statement).all()

            # Create new objects to avoid detached session issues
            sessions = []
            for db_session in result:
                # Force loading of attributes while session is still active
                session_id = db_session.id
                session_title = db_session.title
                session_user_id = db_session.user_id
                session_is_active = db_session.is_active
                session_created_at = db_session.created_at
                session_updated_at = db_session.updated_at

                # Create a new object with loaded values
                new_session = ChatSession(
                    id=session_id,
                    user_id=session_user_id,
                    title=session_title,
                    is_active=session_is_active
                )
                new_session.created_at = session_created_at
                new_session.updated_at = session_updated_at
                sessions.append(new_session)

            return sessions

    async def validate_user_owns_session(self, user_id: UUID, session_id: UUID) -> bool:
        """Validate that a user owns a specific chat session."""
        session = await self.get_session_for_user(session_id, user_id)
        return session is not None

    async def deactivate_session(self, session_id: UUID) -> bool:
        """Deactivate a chat session."""
        with get_session_context() as session:
            statement = select(ChatSession).where(ChatSession.id == session_id)
            db_session = session.exec(statement).first()

            if not db_session:
                return False

            db_session.is_active = False
            db_session.updated_at = datetime.now()
            session.add(db_session)
            session.commit()
            return True

    async def add_message(self, session_id: UUID, role: MessageRole, content: str) -> ChatMessage:
        """Add a message to a chat session."""
        with get_session_context() as session:
            # Verify session exists
            session_check = select(ChatSession).where(ChatSession.id == session_id)
            db_session = session.exec(session_check).first()

            if not db_session:
                raise ValueError(f"Session {session_id} not found")

            # Create new message
            db_message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content
            )

            session.add(db_message)
            session.commit()
            session.refresh(db_message)

            # Create a new object to avoid detached session issues
            message_id = db_message.id
            message_session_id = db_message.session_id
            message_role = db_message.role
            message_content = db_message.content
            message_timestamp = db_message.timestamp
            message_metadata = db_message.message_metadata
            message_created_at = db_message.created_at
            message_updated_at = db_message.updated_at

            # Create a new object with loaded values
            new_message = ChatMessage(
                id=message_id,
                session_id=message_session_id,
                role=message_role,
                content=message_content,
                timestamp=message_timestamp,
                message_metadata=message_metadata
            )
            new_message.created_at = message_created_at
            new_message.updated_at = message_updated_at

            return new_message

    async def get_messages(self, session_id: UUID, limit: int = 100, offset: int = 0) -> List[ChatMessage]:
        """Get messages for a specific session with pagination."""
        with get_session_context() as session:
            statement = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.asc())
                .offset(offset)
                .limit(limit)
            )
            result = session.exec(statement).all()

            # Create new objects to avoid detached session issues
            messages = []
            for db_message in result:
                # Force loading of attributes while session is still active
                message_id = db_message.id
                message_session_id = db_message.session_id
                message_role = db_message.role
                message_content = db_message.content
                message_timestamp = db_message.timestamp
                message_metadata = db_message.message_metadata
                message_created_at = db_message.created_at
                message_updated_at = db_message.updated_at

                # Create a new object with loaded values
                new_message = ChatMessage(
                    id=message_id,
                    session_id=message_session_id,
                    role=message_role,
                    content=message_content,
                    timestamp=message_timestamp,
                    message_metadata=message_metadata
                )
                new_message.created_at = message_created_at
                new_message.updated_at = message_updated_at
                messages.append(new_message)

            return messages

    async def get_recent_messages(self, session_id: UUID, limit: int = 10) -> List[ChatMessage]:
        """Get the most recent messages for a session."""
        with get_session_context() as session:
            statement = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(limit)
            )
            result = session.exec(statement).all()

            # Create new objects to avoid detached session issues
            messages = []
            for db_message in result:
                # Force loading of attributes while session is still active
                message_id = db_message.id
                message_session_id = db_message.session_id
                message_role = db_message.role
                message_content = db_message.content
                message_timestamp = db_message.timestamp
                message_metadata = db_message.message_metadata
                message_created_at = db_message.created_at
                message_updated_at = db_message.updated_at

                # Create a new object with loaded values
                new_message = ChatMessage(
                    id=message_id,
                    session_id=message_session_id,
                    role=message_role,
                    content=message_content,
                    timestamp=message_timestamp,
                    message_metadata=message_metadata
                )
                new_message.created_at = message_created_at
                new_message.updated_at = message_updated_at
                messages.append(new_message)

            # Reverse to return in chronological order
            return messages[::-1]

    async def add_tool_invocation(
        self,
        session_id: UUID,
        tool_name: str,
        arguments: Dict[str, Any],
        result: Optional[Dict[str, Any]] = None,
        status: InvocationStatus = InvocationStatus.PENDING
    ) -> ToolInvocation:
        """Add a tool invocation record to a session."""
        with get_session_context() as session:
            # Verify session exists
            session_check = select(ChatSession).where(ChatSession.id == session_id)
            db_session = session.exec(session_check).first()

            if not db_session:
                raise ValueError(f"Session {session_id} not found")

            # Ensure session_id is a string for JSON serialization
            session_id_str = str(session_id) if isinstance(session_id, UUID) else session_id

            # Create new tool invocation
            db_invocation = ToolInvocation(
                session_id=session_id_str,
                tool_name=tool_name,
                arguments=json.dumps(arguments),  # Serialize to JSON string
                result=json.dumps(result) if result else None,  # Serialize to JSON string if not None
                status=status
            )

            session.add(db_invocation)
            session.commit()
            session.refresh(db_invocation)

            # Create a new object to avoid detached session issues
            invocation_id = db_invocation.id
            invocation_session_id = db_invocation.session_id
            invocation_tool_name = db_invocation.tool_name
            invocation_arguments = db_invocation.arguments
            invocation_result = db_invocation.result
            invocation_timestamp = db_invocation.timestamp
            invocation_status = db_invocation.status
            invocation_created_at = db_invocation.created_at
            invocation_updated_at = db_invocation.updated_at

            # Deserialize JSON strings back to Python objects
            try:
                deserialized_arguments = json.loads(invocation_arguments) if invocation_arguments else {}
            except (json.JSONDecodeError, TypeError):
                # If it's already a dict or can't be parsed, use as-is
                deserialized_arguments = invocation_arguments if isinstance(invocation_arguments, dict) else {}

            try:
                deserialized_result = json.loads(invocation_result) if invocation_result else None
            except (json.JSONDecodeError, TypeError):
                # If it's already a dict or can't be parsed, use as-is
                deserialized_result = invocation_result if isinstance(invocation_result, dict) else None

            # Ensure session_id is converted to UUID when creating the object
            session_id_obj = UUID(invocation_session_id) if isinstance(invocation_session_id, str) else invocation_session_id

            # Create a new object with loaded values
            new_invocation = ToolInvocation(
                id=invocation_id,
                session_id=session_id_obj,
                tool_name=invocation_tool_name,
                arguments=deserialized_arguments,
                result=deserialized_result,
                timestamp=invocation_timestamp,
                status=invocation_status
            )
            new_invocation.created_at = invocation_created_at
            new_invocation.updated_at = invocation_updated_at

            return new_invocation

    async def update_tool_invocation(
        self,
        invocation_id: UUID,
        result: Optional[Dict[str, Any]] = None,
        status: Optional[InvocationStatus] = None
    ) -> Optional[ToolInvocation]:
        """Update a tool invocation record."""
        with get_session_context() as session:
            statement = select(ToolInvocation).where(ToolInvocation.id == invocation_id)
            db_invocation = session.exec(statement).first()

            if not db_invocation:
                return None

            if result is not None:
                # Ensure any UUIDs in the result are converted to strings
                if isinstance(result, dict):
                    # Convert any UUID values in the result to strings
                    def convert_uuids_to_strings(obj):
                        if isinstance(obj, dict):
                            return {k: convert_uuids_to_strings(v) for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [convert_uuids_to_strings(item) for item in obj]
                        elif isinstance(obj, UUID):
                            return str(obj)
                        else:
                            return obj

                    result = convert_uuids_to_strings(result)

                db_invocation.result = json.dumps(result)  # Serialize to JSON string
            if status is not None:
                db_invocation.status = status

            db_invocation.updated_at = datetime.now()
            session.add(db_invocation)
            session.commit()
            session.refresh(db_invocation)

            import json

            # Create a new object to avoid detached session issues
            invocation_id = db_invocation.id
            invocation_session_id = db_invocation.session_id
            invocation_tool_name = db_invocation.tool_name
            invocation_arguments = db_invocation.arguments
            invocation_result = db_invocation.result
            invocation_timestamp = db_invocation.timestamp
            invocation_status = db_invocation.status
            invocation_created_at = db_invocation.created_at
            invocation_updated_at = db_invocation.updated_at

            # Deserialize JSON strings back to Python objects
            try:
                deserialized_arguments = json.loads(invocation_arguments) if invocation_arguments else {}
            except (json.JSONDecodeError, TypeError):
                # If it's already a dict or can't be parsed, use as-is
                deserialized_arguments = invocation_arguments if isinstance(invocation_arguments, dict) else {}

            try:
                deserialized_result = json.loads(invocation_result) if invocation_result else None
            except (json.JSONDecodeError, TypeError):
                # If it's already a dict or can't be parsed, use as-is
                deserialized_result = invocation_result if isinstance(invocation_result, dict) else None

            # Ensure session_id is converted to UUID when creating the object
            session_id_obj = UUID(invocation_session_id) if isinstance(invocation_session_id, str) else invocation_session_id

            # Create a new object with loaded values
            new_invocation = ToolInvocation(
                id=invocation_id,
                session_id=session_id_obj,
                tool_name=invocation_tool_name,
                arguments=deserialized_arguments,
                result=deserialized_result,
                timestamp=invocation_timestamp,
                status=invocation_status
            )
            new_invocation.created_at = invocation_created_at
            new_invocation.updated_at = invocation_updated_at

            return new_invocation

    async def get_tool_invocations(self, session_id: UUID) -> List[ToolInvocation]:
        """Get all tool invocations for a session."""
        with get_session_context() as session:
            statement = (
                select(ToolInvocation)
                .where(ToolInvocation.session_id == session_id)
                .order_by(ToolInvocation.timestamp.desc())
            )
            result = session.exec(statement).all()

            # Create new objects to avoid detached session issues
            invocations = []
            for db_invocation in result:
                # Force loading of attributes while session is still active
                invocation_id = db_invocation.id
                invocation_session_id = db_invocation.session_id
                invocation_tool_name = db_invocation.tool_name
                invocation_arguments = db_invocation.arguments
                invocation_result = db_invocation.result
                invocation_timestamp = db_invocation.timestamp
                invocation_status = db_invocation.status
                invocation_created_at = db_invocation.created_at
                invocation_updated_at = db_invocation.updated_at

                # Deserialize JSON strings back to Python objects
                try:
                    deserialized_arguments = json.loads(invocation_arguments) if invocation_arguments else {}
                except (json.JSONDecodeError, TypeError):
                    # If it's already a dict or can't be parsed, use as-is
                    deserialized_arguments = invocation_arguments if isinstance(invocation_arguments, dict) else {}

                try:
                    deserialized_result = json.loads(invocation_result) if invocation_result else None
                except (json.JSONDecodeError, TypeError):
                    # If it's already a dict or can't be parsed, use as-is
                    deserialized_result = invocation_result if isinstance(invocation_result, dict) else None

                # Ensure session_id is converted to UUID when creating the object
                session_id_obj = UUID(invocation_session_id) if isinstance(invocation_session_id, str) else invocation_session_id

                # Create a new object with loaded values
                new_invocation = ToolInvocation(
                    id=invocation_id,
                    session_id=session_id_obj,
                    tool_name=invocation_tool_name,
                    arguments=deserialized_arguments,
                    result=deserialized_result,
                    timestamp=invocation_timestamp,
                    status=invocation_status
                )
                new_invocation.created_at = invocation_created_at
                new_invocation.updated_at = invocation_updated_at
                invocations.append(new_invocation)

            return invocations

    async def get_session_summary(self, session_id: UUID) -> Dict[str, Any]:
        """Get a summary of a session including message count and last activity."""
        with get_session_context() as session:
            # Get the session
            session_stmt = select(ChatSession).where(ChatSession.id == session_id)
            db_session = session.exec(session_stmt).first()

            if not db_session:
                return {}

            # Count messages
            message_count_stmt = select(ChatMessage).where(ChatMessage.session_id == session_id)
            message_count = len(session.exec(message_count_stmt).all())

            # Get last message time
            last_message_stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(1)
            )
            last_message = session.exec(last_message_stmt).first()

            return {
                "session": db_session,
                "message_count": message_count,
                "last_activity": last_message.timestamp if last_message else db_session.updated_at,
                "is_active": db_session.is_active
            }

    async def archive_old_messages(self, session_id: UUID, max_messages: int = 1000) -> int:
        """Archive old messages to keep session size manageable."""
        with get_session_context() as session:
            # Get all messages for the session
            stmt = (
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.asc())
            )
            all_messages = session.exec(stmt).all()

            # If we have more than max_messages, mark older ones as archived
            if len(all_messages) > max_messages:
                messages_to_remove = len(all_messages) - max_messages
                for i in range(messages_to_remove):
                    session.delete(all_messages[i])
                session.commit()
                return messages_to_remove

            return 0


# Global instance of the chat service
chat_service = ChatService()