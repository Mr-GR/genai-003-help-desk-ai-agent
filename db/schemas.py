from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
import re

class TicketBase(BaseModel):
    user_ticket: str  # Required now
    agent_response: Optional[str] = None

class TicketCreate(TicketBase):
    pass  # inherit, no re-declare fields

class TicketResponse(TicketBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    user_message: Optional[str]
    ai_response: Optional[str]

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(BaseModel):
    id: int
    user_message: str
    ai_response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character.")
        return password

class UserResponse(UserBase):
    id: int
    tickets: List[TicketResponse] = []
    chat_messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: str
    user_id: int
