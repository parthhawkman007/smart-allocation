from fastapi import FastAPI
from app.api.routes import report
from app.api.routes import ngo
from app.api.routes import volunteer
from app.api.routes import auth


app = FastAPI()

app.include_router(report.router)
app.include_router(ngo.router)
app.include_router(volunteer.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "API Running 🚀"}