from sqlalchemy.orm import Session 
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int, response: str):
    db_ticket = models.Ticket(ticket=ticket.ticket, response=response, owner_id=user_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def create_chat_message(db: Session, user_id: int, content: str, role: str):
    db_message = models.ChatMessage(
        user_id=user_id,
        content=content,
        role=role
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message



def get_chat_history(db: Session, user_id: int, limit: int = 50):
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == user_id)
        .order_by(models.ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )
