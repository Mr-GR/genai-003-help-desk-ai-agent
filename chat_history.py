from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, database
from dependencies import get_current_user
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    role: str 
    content: str
    created_at: datetime 
    class Config:
        orm_mode = True  

class NewChatMessageRequest(BaseModel):
    role: str 
    content: str

@router.get("/chat-messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    chat_messages = db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == current_user.id
    ).order_by(models.ChatMessage.created_at.desc()).all()
    return chat_messages

@router.post("/chat-messages", response_model=ChatMessageResponse)
async def create_chat_message(
    new_message: NewChatMessageRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    message = models.ChatMessage(
        user_id=current_user.id,
        role=new_message.role,
        content=new_message.content,
        created_at=datetime.utcnow()
    )

    db.add(message)
    db.commit()
    db.refresh(message)
    return message

@router.delete("/chat-messages", status_code=204)
async def delete_all_chat_messages(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted = db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == current_user.id
    ).delete()
    db.commit()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="No chat history found to delete.")
    return

@router.delete("/chat-messages/{message_id}", status_code=204)
async def delete_chat_message_by_id(
    message_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    message = db.query(models.ChatMessage).filter(
        models.ChatMessage.id == message_id,
        models.ChatMessage.user_id == current_user.id
    ).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found.")
    
    db.delete(message)
    db.commit()
    return
