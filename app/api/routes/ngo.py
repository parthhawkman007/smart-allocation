from fastapi import APIRouter
from app.database.queries import get_all_reports

router = APIRouter()

@router.get("/ngo-reports")
def get_ngo_reports():
    reports = get_all_reports()
    return {"reports": reports}