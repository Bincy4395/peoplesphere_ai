
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationSummary,
)

from schemas.chat import ChatMessageHistory

from ai_langchain.lc_rag_service import generate_rag_answer

from services.chat_history_service import (
    save_chat_message,
    get_chat_history,
    get_employee_conversations,
    get_conversation_messages,
)


# --------------------------------------------------
# 1. Create LangChain chat router
# --------------------------------------------------
router = APIRouter(
    prefix="/chat-langchain",
    tags=["LangChain Chatbot"],
)


# --------------------------------------------------
# 2. LangChain Chat API endpoint
# --------------------------------------------------
@router.post("/", response_model=ChatResponse)
async def chat_with_langchain(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    try:
        employee_id = request.employee_id

        conversation_id = (
            request.conversation_id
            or str(uuid4())
        )

        # Get previous conversation history
        previous_messages = get_chat_history(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
        )

        chat_history = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in previous_messages
        ]

        # Save user message
        save_chat_message(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
            role="user",
            content=request.message,
        )

        # Generate answer using LangChain RAG
        result = generate_rag_answer(
            question=request.message,
            chat_history=chat_history,
        )

        # Save assistant response
        save_chat_message(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"],
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conversation_id,
            has_relevant_context=result[
                "has_relevant_context"
            ],
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"LangChain AI service error: {str(e)}",
        )


# --------------------------------------------------
# 3. Get Employee Conversations
# --------------------------------------------------
@router.get(
    "/conversations",
    response_model=list[ConversationSummary],
)
async def get_langchain_conversations(
    employee_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_employee_conversations(
            db=db,
            employee_id=employee_id,
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve conversations: {str(e)}",
        )


# --------------------------------------------------
# 4. Get Conversation Messages
# --------------------------------------------------
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[ChatMessageHistory],
)
async def get_langchain_messages(
    conversation_id: str,
    employee_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_conversation_messages(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
        )

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve chat messages: {str(e)}",
        )
