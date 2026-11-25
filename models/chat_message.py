from datetime import datetime

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# --------------------------------------------------
# 1. Chat Message Model
# --------------------------------------------------
class ChatMessage(Base):

    __tablename__ = "chat_messages"

    # --------------------------------------------------
    # 2. Message ID
    # --------------------------------------------------
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # --------------------------------------------------
    # 3. Employee ID
    # --------------------------------------------------
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # 4. Conversation ID
    # --------------------------------------------------
    conversation_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # 5. Message Role
    # --------------------------------------------------
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    # --------------------------------------------------
    # 6. Message Content
    # --------------------------------------------------
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # --------------------------------------------------
    # 7. Created At
    # --------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )