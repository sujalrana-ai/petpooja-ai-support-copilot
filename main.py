from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from support_engine import diagnose

app = FastAPI(
    title="AI Support & Incident Diagnosis Copilot API",
    description="Independent incident diagnosis portfolio prototype",
    version="0.1.0"
)


class IncidentRequest(BaseModel):
    description: str = Field(min_length=3, max_length=2000)
    logs: str = Field(default="", max_length=10000)


@app.get("/")
def home():
    return {
        "project": "AI Support & Incident Diagnosis Copilot",
        "status": "running",
        "mode": "portfolio_prototype"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/diagnose")
def analyze_incident(request: IncidentRequest):
    try:
        return diagnose(request.description, request.logs)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

