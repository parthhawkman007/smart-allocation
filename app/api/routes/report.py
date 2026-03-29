from fastapi import APIRouter
from app.database.queries import update_report_status
from fastapi import UploadFile, File

router = APIRouter()

@router.patch("/report-status/{report_id}")
def update_status(report_id: str, status: str):
    updated = update_report_status(report_id, status)
    return {"updated": updated}

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename,
            "ai_result": {
                "category": "waste",
                "urgency": "high",
                "best_ngo": "Clean City NGO",
                "matched_volunteers": 5
            }}