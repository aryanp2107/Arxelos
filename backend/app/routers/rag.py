"""
Model 3 — RAG Medical Literature Q&A
Routes for natural language queries against medical literature.
Activate in main.py when the RAG pipeline is ready (target: Week 5-6).
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5  # Number of source chunks to retrieve
    model: str = "gpt-4o-mini"  # LLM for answer generation


class SourceChunk(BaseModel):
    text: str
    source: str  # e.g., PubMed ID or paper title
    relevance_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    model_used: str


@router.post("/ask")
async def ask_medical_question(request: QueryRequest):
    """
    Submit a medical question. The RAG pipeline retrieves relevant
    literature chunks and generates a cited answer.
    """
    return {
        "status": "stub",
        "message": "Model 3 endpoint scaffolded — RAG pipeline not yet connected.",
        "question": request.question,
    }
