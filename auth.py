from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

auth_router = APIRouter()

USERS = {
    "admin": "adminpass",
    "user1": "test123",
    "demo": "demo"
}

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@auth_router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    username = payload.username
    password = payload.password


    if username in USERS and USERS[username] == password:
        return {
            "access_token": f"token_for_{username}",
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")
