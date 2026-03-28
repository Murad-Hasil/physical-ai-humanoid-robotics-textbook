"""
Chat API endpoint with hardware-aware personalization.

Provides the main chat interface for the RAG system.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import get_current_user, UserContext

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Chat"])


class ChatRequest(BaseModel):
    """Chat request model. Accepts both 'query' and 'message' field names."""
    query: Optional[str] = None
    message: Optional[str] = None
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None

    @model_validator(mode="after")
    def resolve_query(self):
        """Resolve query from either 'query' or 'message' field."""
        if not self.query and self.message:
            self.query = self.message
        if not self.query:
            raise ValueError("Either 'query' or 'message' field is required")
        return self


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    sources: list = []
    confidence: float = 0.0
    session_id: Optional[str] = None
    hardware_context_used: bool = False
    hardware_type: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: Optional[UserContext] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Chat endpoint with optional authentication.

    Works for both guests (no auth) and authenticated users.
    Authenticated users get hardware-aware personalized responses.

    **Request:**
    - `query` or `message`: User's question
    - `selected_text`: Optional selected text from page
    - `session_id` or `conversation_id`: Optional session ID

    **Response:**
    - `response`: AI-generated answer
    - `sources`: Source attributions
    - `confidence`: Confidence score
    - `hardware_context_used`: Whether hardware profile was used
    """
    user_id = str(user.user_id) if user else None
    session_id = request.session_id or request.conversation_id

    logger.info(f"Chat request from user {user_id or 'guest'}: {request.query[:100]}...")

    try:
        from services.rag_pipeline import RAGPipeline
        pipeline = RAGPipeline(db)
        result = await pipeline.process_query(
            query=request.query,
            user_id=user_id,
            selected_text=request.selected_text,
            session_id=session_id,
        )

        return ChatResponse(
            response=result.get("response", "Sorry, I could not generate a response."),
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0),
            session_id=result.get("session_id"),
            hardware_context_used=result.get("hardware_context_used", False),
            hardware_type=result.get("hardware_type"),
        )

    except Exception as e:
        logger.error(f"Chat pipeline error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "chat_error",
                "message": f"Failed to process your query: {str(e)}",
            },
        )
