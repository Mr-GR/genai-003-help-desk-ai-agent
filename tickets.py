from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas, crud  # adjust if your folder structure is different
from db.database import get_db  # ✅ Correct import
from dependencies import get_current_user  # ✅ Already correct
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class TicketResponse(BaseModel):
    id: int
    ticket: str
    response: str | None
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/tickets", response_model=TicketResponse)
def submit_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_ticket = crud.create_ticket(db, ticket, current_user.id, response=None)
    return new_ticket

@router.get("/tickets", response_model=List[TicketResponse])
def get_user_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Ticket).filter(models.Ticket.owner_id == current_user.id).all()
