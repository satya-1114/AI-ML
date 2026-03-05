from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
    version="1.0.0",
    description="Mock interview answer evaluator using TF-IDF + cosine similarity.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([reference_answer, payload.answer])

    similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    score = round(similarity * 100)

    if similarity > 0.75:
        evaluation = "Correct"
        feedback = "Great answer. You captured the core concept clearly."
    elif similarity > 0.45:
        evaluation = "Partially Correct"
        feedback = "Decent attempt. Include more key terms and precise details."
    else:
        evaluation = "Incorrect"
        feedback = "Answer misses key points. Review the core concept and try again."

    return EvaluateResponse(score=score, evaluation=evaluation, feedback=feedback)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
