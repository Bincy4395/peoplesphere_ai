
from datetime import datetime

from pydantic import BaseModel, Field


# --------------------------------------------------
# 1. Chat request schema
# --------------------------------------------------
class ChatRequest(BaseModel):

    message: str = Field(min_length=1)

    conversation_id: str | None = None

    employee_id: int


# --------------------------------------------------
# 2. Chat source schema
# --------------------------------------------------
class ChatSource(BaseModel):

    source: str | None = None

    category: str | None = None

    department: str | None = None


# --------------------------------------------------
# 3. Chat response schema
# --------------------------------------------------
class ChatResponse(BaseModel):

    answer: str

    sources: list[ChatSource] = Field(
        default_factory=list
    )

    conversation_id: str

    has_relevant_context: bool


# --------------------------------------------------
# 4. Conversation summary schema
# --------------------------------------------------
class ConversationSummary(BaseModel):

    conversation_id: str

    last_message: str

    updated_at: datetime

# --------------------------------------------------
# 5. Chat message history schema
# --------------------------------------------------
class ChatMessageHistory(BaseModel):

    id: int

    role: str

    content: str

    created_at: datetime