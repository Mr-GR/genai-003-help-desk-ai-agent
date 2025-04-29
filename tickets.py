from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas, crud
from db.database import get_db
from dependencies import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

def generate_ticket_title(text: str) -> str:
    """Generate a short title for the ticket based on the first few words."""
    if not text:
        return "Untitled Ticket"
    return text.strip()[:50] + ("..." if len(text) > 50 else "")



@router.post("/tickets", response_model=schemas.TicketResponse)
def create_ticket(
    new_ticket: schemas.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ticket = models.Ticket(
        title=generate_ticket_title(new_ticket.user_ticket),
        user_ticket=new_ticket.user_ticket,
        agent_response=new_ticket.agent_response,
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/tickets", response_model=List[schemas.TicketResponse])
def get_user_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Ticket).filter(
        models.Ticket.owner_id == current_user.id
    ).order_by(models.Ticket.created_at.desc()).all()

@router.delete("/tickets", status_code=204)
def delete_all_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted = db.query(models.Ticket).filter(
        models.Ticket.owner_id == current_user.id
    ).delete()
    db.commit()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="No ticket history found to delete.")
    return

@router.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket_by_id(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id,
        models.Ticket.owner_id == current_user.id
    ).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")

    db.delete(ticket)
    db.commit()
    return
