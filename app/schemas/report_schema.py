from pydantic import BaseModel
from typing import Optional

class ReportCreate(BaseModel):
    description: str
    location: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None