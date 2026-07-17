"""FastAPI endpoint for the PCA Cognitive DNA prototype."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, List, Dict, Optional
from enum import Enum

from .llm import BaseLLMAdapter, OllamaAdapter, OpenAIAdapter, GeminiAdapter, OllamaUnavailable
from .config import APP_NAME, VERSION, settings
from .orchestrator import Orchestrator

class LLMProvider(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"

# Global orchestrator instance (default to settings from config.yaml)
def get_orchestrator(llm_provider: Optional[LLMProvider] = None, llm_model: Optional[str] = None) -> Orchestrator:
    # Use settings from config.yaml if not provided in request
    llm_provider = llm_provider or LLMProvider(settings["llm"]["provider"])
    llm_model = llm_model or settings["llm"]["model"]
    temperature = settings["llm"].get("temperature", 0.7)

    llm_adapter: BaseLLMAdapter
    if llm_provider == LLMProvider.OLLAMA:
        llm_adapter = OllamaAdapter(model=llm_model, temperature=temperature)
    elif llm_provider == LLMProvider.OPENAI:
        llm_adapter = OpenAIAdapter(model=llm_model, temperature=temperature)
    elif llm_provider == LLMProvider.GEMINI:
        llm_adapter = GeminiAdapter(model=llm_model, temperature=temperature)
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")
    return Orchestrator(llm=llm_adapter)

orchestrator_instance = get_orchestrator()
orchestrator_instance.start()

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="API for PCA Cognitive DNA prototype"
)

class AnalyzeRequest(BaseModel):
    llm_provider: Optional[LLMProvider] = None
    llm_model: Optional[str] = None
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
        # Re-initialize orchestrator with selected LLM provider/model for each request
        current_orchestrator = get_orchestrator(request.llm_provider, request.llm_model)
        state = current_orchestrator.think(request.question)
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
