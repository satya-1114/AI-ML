from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# NEW: semantic embedding model
from sentence_transformers import SentenceTransformer, util


BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "dataset" / "questions.json"


class QuestionItem(BaseModel):
    question: str
    reference_answer: str


class EvaluateRequest(BaseModel):
    question: str = Field(..., min_length=3)
    answer: str = Field(..., min_length=3)


class EvaluateResponse(BaseModel):
    score: int
    evaluation: str
    feedback: str


app = FastAPI(
    title="InterviewSense AI API",
    version="1.1.0",
    description="Mock interview evaluator using semantic embeddings.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load embedding model once when server starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_questions() -> List[QuestionItem]:
    with DATASET_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [QuestionItem(**item) for item in data]


QUESTIONS = load_questions()
QUESTION_MAP: Dict[str, str] = {item.question: item.reference_answer for item in QUESTIONS}


@app.get("/questions", response_model=List[str])
def get_questions() -> List[str]:
    return [item.question for item in QUESTIONS]


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate_answer(payload: EvaluateRequest) -> EvaluateResponse:
    if payload.question not in QUESTION_MAP:
        raise HTTPException(status_code=404, detail="Question not found")

    reference_answer = QUESTION_MAP[payload.question]

    # NEW: semantic similarity instead of TF-IDF
    ref_embedding = model.encode(reference_answer, convert_to_tensor=True)
    user_embedding = model.encode(payload.answer, convert_to_tensor=True)

    similarity = float(util.cos_sim(ref_embedding, user_embedding).item())

    score = round(similarity * 100)

    if similarity > 0.75:
        evaluation = "Correct"
        feedback = "Great answer. You captured the core concept clearly."
    elif similarity > 0.45:
        evaluation = "Partially Correct"
        feedback = "Decent attempt. Include more key ideas and deeper explanation."
    else:
        evaluation = "Incorrect"
        feedback = "Answer misses important concepts. Review the topic and try again."

    return EvaluateResponse(score=score, evaluation=evaluation, feedback=feedback)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}