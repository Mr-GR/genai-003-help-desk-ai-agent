from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TicketBase(BaseModel):
    ticket: str

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    response: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    tickets: List[TicketResponse] = []

    class Config:
        from_attributes = True
