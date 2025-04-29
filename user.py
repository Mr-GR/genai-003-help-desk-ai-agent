from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import get_db
from dependencies import get_current_user

router = APIRouter()

@router.get("/user", response_model=schemas.UserResponse)
def get_current_user_info(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return current_user
