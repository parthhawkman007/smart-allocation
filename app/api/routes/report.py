from fastapi import APIRouter, UploadFile, File
from app.database.queries import update_report_status

router = APIRouter()

# ✅ Update report status
@router.patch("/report-status/{report_id}")
def update_status(report_id: str, status: str):
    updated = update_report_status(report_id, status)
    return {"updated": updated}


# ✅ Upload image + AI result (current static version)
@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "ai_result": {
            "category": "waste",
            "urgency": "high",
            "best_ngo": "Clean City NGO",
            "matched_volunteers": 5
        }
    }