
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationSummary
)

from ai.rag_service import generate_rag_answer

from services.chat_history_service import (
    save_chat_message,
    get_chat_history,
    get_employee_conversations
)

from schemas.chat import ChatMessageHistory

from services.chat_history_service import (
    get_conversation_messages
)

# --------------------------------------------------
# 1. Create chat router
# --------------------------------------------------
router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"]
)


# --------------------------------------------------
# 2. Chat API endpoint
# --------------------------------------------------
@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    try:

        # --------------------------------------------------
        # 3. Get employee ID
        # --------------------------------------------------
        employee_id = request.employee_id

        # --------------------------------------------------
        # 4. Get or create conversation ID
        # --------------------------------------------------
        conversation_id = (
            request.conversation_id
            or str(uuid4())
        )

        # --------------------------------------------------
        # 5. Retrieve previous conversation history
        # --------------------------------------------------
        previous_messages = get_chat_history(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id
        )

        chat_history = [
            {
                "role": message.role,
                "content": message.content
            }
            for message in previous_messages
        ]

        # --------------------------------------------------
        # 6. Save user message
        # --------------------------------------------------
        save_chat_message(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )

        # --------------------------------------------------
        # 7. Generate RAG answer
        # --------------------------------------------------
        result = generate_rag_answer(
            question=request.message,
            chat_history=chat_history
        )

        # --------------------------------------------------
        # 8. Save assistant response
        # --------------------------------------------------
        save_chat_message(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"]
        )

        # --------------------------------------------------
        # 9. Return answer and sources
        # --------------------------------------------------
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            conversation_id=conversation_id,
            has_relevant_context=result["has_relevant_context"]
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )


# --------------------------------------------------
# 10. Get Employee Conversations
# --------------------------------------------------
@router.get(
    "/conversations",
    response_model=list[ConversationSummary]
)
async def get_conversations(
    employee_id: int,
    db: Session = Depends(get_db)
):

    try:

        conversations = get_employee_conversations(
            db=db,
            employee_id=employee_id
        )

        return conversations

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve conversations: {str(e)}"
        )

# --------------------------------------------------
# 11. Get Messages of a Conversation
# --------------------------------------------------
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[ChatMessageHistory]
)
async def get_messages(
    conversation_id: str,
    employee_id: int,
    db: Session = Depends(get_db)
):

    try:

        messages = get_conversation_messages(
            db=db,
            employee_id=employee_id,
            conversation_id=conversation_id
        )

        return messages

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve chat messages: {str(e)}"
        )
