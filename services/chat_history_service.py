
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.chat_message import ChatMessage


# --------------------------------------------------
# 1. Save Chat Message
# --------------------------------------------------
def save_chat_message(
    db: Session,
    employee_id: int,
    conversation_id: str,
    role: str,
    content: str
):
    chat_message = ChatMessage(
        employee_id=employee_id,
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)

    return chat_message


# --------------------------------------------------
# 2. Get Chat History
# --------------------------------------------------
def get_chat_history(
    db: Session,
    employee_id: int,
    conversation_id: str
):
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.employee_id == employee_id,
            ChatMessage.conversation_id == conversation_id
        )
        .order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc()
        )
        .all()
    )

    return messages


# --------------------------------------------------
# 3. Get Employee Conversations
# --------------------------------------------------
def get_employee_conversations(
    db: Session,
    employee_id: int
):
    conversation_rows = (
        db.query(
            ChatMessage.conversation_id,
            func.max(
                ChatMessage.created_at
            ).label("updated_at")
        )
        .filter(
            ChatMessage.employee_id == employee_id
        )
        .group_by(
            ChatMessage.conversation_id
        )
        .order_by(
            func.max(
                ChatMessage.created_at
            ).desc()
        )
        .all()
    )

    conversations = []

    for row in conversation_rows:

        latest_message = (
            db.query(ChatMessage)
            .filter(
                ChatMessage.employee_id == employee_id,
                ChatMessage.conversation_id
                == row.conversation_id
            )
            .order_by(
                ChatMessage.id.desc()
            )
            .first()
        )

        if latest_message:

            conversations.append({
                "conversation_id": row.conversation_id,
                "last_message": latest_message.content,
                "updated_at": row.updated_at
            })

    return conversations

# --------------------------------------------------
# 4. Get Conversation Messages
# --------------------------------------------------
def get_conversation_messages(
    db: Session,
    employee_id: int,
    conversation_id: str
):
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.employee_id == employee_id,
            ChatMessage.conversation_id == conversation_id
        )
        .order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc()
        )
        .all()
    )

    return messages