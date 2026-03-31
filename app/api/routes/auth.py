from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# TEMP DB (later replace with real DB)
users_db = []

class User(BaseModel):
    email: str
    password: str
    role: str  # user / ngo / volunteer


@router.post("/signup")
def signup(user: User):
    users_db.append(user.dict())
    return {"message": "User created successfully"}


@router.post("/login")
def login(user: User):
    for u in users_db:
        if u["email"] == user.email and u["password"] == user.password:
            return {"message": "Login success", "role": u["role"]}
    
    return {"error": "Invalid credentials"}