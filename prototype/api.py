api_code = '''"""FastAPI endpoint for the PCA Cognitive DNA prototype."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, List, Dict

from .config import APP_NAME, VERSION
from .orchestrator import Orchestrator

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="API for PCA Cognitive DNA prototype"
)

orchestrator = Orchestrator()
orchestrator.start()

class AnalyzeRequest(BaseModel):
    question: str

class AnalyzeResponse(BaseModel):
    question: str
    response: str
    trace: List[Dict[str, Any]]
    notes: List[str]

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    try:
        state = orchestrator.think(request.question)
        return AnalyzeResponse(
            question=state.user_input,
            response=state.response,
            trace=state.trace,
            notes=state.notes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "version": VERSION}
'''

with open("prototype/api.py", "w") as f:
    f.write(api_code)
