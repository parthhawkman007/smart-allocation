from fastapi import APIRouter
from app.database.queries import get_volunteer_tasks

router = APIRouter()

@router.get("/volunteer-tasks/{name}")
def volunteer_tasks(name: str):
    tasks = get_volunteer_tasks(name)
    return {"tasks": tasks}