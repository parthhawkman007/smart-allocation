from fastapi import APIRouter
from pydantic import BaseModel
from app.database.supabase_client import supabase

router = APIRouter()


class User(BaseModel):
    email: str
    password: str
    role: str


# 🔥 SIGNUP
@router.post("/signup")
def signup(user: User):
    # ✅ CHECK IF USER ALREADY EXISTS
    existing = supabase.table("users").select("*").eq("email", user.email).execute()

    if existing.data:
        return {"error": "User already exists"}

    # ✅ INSERT NEW USER
    supabase.table("users").insert({
        "email": user.email,
        "password": user.password,
        "role": user.role,
        "name": "temp",
        "location": "temp"
    }).execute()

    return {"message": "User created successfully"}


# 🔥 LOGIN
@router.post("/login")
def login(user: User):
    res = supabase.table("users").select("*").eq("email", user.email).execute()

    if not res.data:
        return {"error": "User not found"}

    db_user = res.data[0]

    # ✅ PASSWORD CHECK
    if db_user["password"] != user.password:
        return {"error": "Invalid password"}

    return {
        "message": "Login success",
        "role": db_user["role"]
    }