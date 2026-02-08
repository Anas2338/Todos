"""Chat API endpoints for natural language todo management."""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime
import json

from ..core.auth import get_current_user, get_optional_user
from ..core.rate_limiter import check_rate_limit
from ..services.chat_service import chat_service
from ..chat.agent import ai_agent
from ..models.chat_message import MessageRole


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/sessions")
async def create_or_continue_session(
    request: Request,
    data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Start a new chat session or continue an existing one.
    """
    # Extract data from request
    user_message = data.get("message")
    session_id_str = data.get("session_id")

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Get user ID from current user
    user_id = current_user["user_id"]

    # Validate session_id if provided
    session_id = None
    if session_id_str:
        try:
            session_id = UUID(session_id_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid session ID format")

    # Check rate limit
    await check_rate_limit(request, user_id)

    # Get or create session
    if session_id:
        # Verify that the session belongs to the user
        session = await chat_service.get_session_for_user(session_id, user_id)
        if not session:
            raise HTTPException(status_code=403, detail="Session not found or unauthorized access")
        db_session_id = session_id
    else:
        # Create new session
        db_session_id = await chat_service.create_session(user_id)

    # Add user message to the session
    await chat_service.add_message(
        session_id=db_session_id,
        role=MessageRole.USER,
        content=user_message
    )

    # Process the message with the AI agent
    try:
        ai_response = await ai_agent.process_message(db_session_id, user_message, user_id=user_id)

        # Add AI response to the chat history
        await chat_service.add_message(
            session_id=db_session_id,
            role=MessageRole.ASSISTANT,
            content=ai_response
        )

        # Prepare response data
        response_data = {
            "session_id": str(db_session_id),
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing message: {str(e)}")

        # Handle specific LLM unavailability
        if "LLM" in str(e) or "connection" in str(e).lower():
            ai_response = "I'm sorry, but I'm currently unable to process your request. The AI service may be temporarily unavailable. Please try again later."

            # Add error message to the chat history
            await chat_service.add_message(
                session_id=db_session_id,
                role=MessageRole.ASSISTANT,
                content=ai_response
            )

            # Prepare response data with error message
            response_data = {
                "session_id": str(db_session_id),
                "response": ai_response,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Error processing your message")

    # Add rate limit headers to response
    response_headers = {}
    if hasattr(request.state, 'rate_limit_remaining'):
        response_headers["X-RateLimit-Remaining"] = str(request.state.rate_limit_remaining)
    if hasattr(request.state, 'rate_limit_reset'):
        response_headers["X-RateLimit-Reset"] = str(request.state.rate_limit_reset)

    # Return response with headers
    from fastapi.responses import JSONResponse
    return JSONResponse(content=response_data, headers=response_headers)


@router.get("/sessions")
async def get_user_sessions(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Retrieve a list of user's chat sessions.
    """
    user_id = current_user["user_id"]

    # Get all sessions for the user
    sessions = await chat_service.get_sessions_for_user(user_id)

    # Format response
    formatted_sessions = []
    for session in sessions:
        formatted_sessions.append({
            "id": str(session.id),
            "title": session.title,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "is_active": session.is_active
        })

    return {
        "sessions": formatted_sessions,
        "total_count": len(formatted_sessions)
    }


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    limit: int = 100,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Retrieve messages from a specific chat session.
    """
    try:
        session_uuid = UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    user_id = current_user["user_id"]

    # Verify that the session belongs to the user
    session = await chat_service.get_session_for_user(session_uuid, user_id)
    if not session:
        raise HTTPException(status_code=403, detail="Session not found or unauthorized access")

    # Get messages for the session
    messages = await chat_service.get_messages(session_uuid, limit=limit, offset=offset)

    # Format response
    formatted_messages = []
    for message in messages:
        formatted_messages.append({
            "id": str(message.id),
            "role": message.role.value,
            "content": message.content,
            "timestamp": message.timestamp.isoformat()
        })

    return {
        "messages": formatted_messages,
        "total_count": len(formatted_messages)
    }


@router.get("/sessions/{session_id}")
async def get_session_details(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get details about a specific chat session.
    """
    try:
        session_uuid = UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    user_id = current_user["user_id"]

    # Verify that the session belongs to the user
    session = await chat_service.get_session_for_user(session_uuid, user_id)
    if not session:
        raise HTTPException(status_code=403, detail="Session not found or unauthorized access")

    # Get session summary
    summary = await chat_service.get_session_summary(session_uuid)

    if not summary:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session": {
            "id": str(summary["session"].id),
            "title": summary["session"].title,
            "created_at": summary["session"].created_at.isoformat(),
            "updated_at": summary["session"].updated_at.isoformat(),
            "is_active": summary["session"].is_active
        },
        "message_count": summary["message_count"],
        "last_activity": summary["last_activity"].isoformat(),
        "is_active": summary["is_active"]
    }


@router.delete("/sessions/{session_id}")
async def deactivate_session(
    session_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Deactivate a chat session.
    """
    try:
        session_uuid = UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID format")

    user_id = current_user["user_id"]

    # Verify that the session belongs to the user
    session = await chat_service.get_session_for_user(session_uuid, user_id)
    if not session:
        raise HTTPException(status_code=403, detail="Session not found or unauthorized access")

    # Deactivate the session
    success = await chat_service.deactivate_session(session_uuid)

    if not success:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "success": True,
        "message": "Session deactivated successfully"
    }