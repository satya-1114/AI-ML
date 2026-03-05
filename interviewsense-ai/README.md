# InterviewSense AI

InterviewSense AI is a beginner-friendly yet recruiter-ready project that simulates an AI-powered mock interview evaluator. A user selects a technical question, writes an answer, and receives an automated score, correctness level, and feedback.

## Project Structure

```bash
interviewsense-ai
├── backend
│   ├── main.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src
│       ├── App.jsx
│       ├── main.jsx
│       └── styles.css
├── dataset
│   └── questions.json
└── README.md
```

## Architecture

- **Frontend (React + Vite):** Modern SaaS-style UI for selecting questions and submitting answers.
- **Backend (FastAPI):** API layer that serves questions and evaluates answers.
- **AI Logic (scikit-learn):** Uses TF-IDF vectorization and cosine similarity to compare candidate answer against a reference answer.
- **Dataset (JSON):** Stores interview questions with reference answers.

## How Evaluation Works

1. User selects a question and writes an answer.
2. Backend loads the matching reference answer.
3. Both reference and user answers are vectorized using **TF-IDF**.
4. **Cosine similarity** is calculated.
5. Similarity is converted into score and label:
   - `similarity > 0.75` → **Correct**
   - `similarity > 0.45` → **Partially Correct**
   - else → **Incorrect**

## API Endpoints

### `GET /questions`
Returns a list of available interview questions.

### `POST /evaluate`
Evaluates a candidate answer.

Request:

```json
{
  "question": "What is a REST API?",
  "answer": "REST API is an architectural style for web services using HTTP methods"
}
```

Response:

```json
{
  "score": 82,
  "evaluation": "Correct",
  "feedback": "Answer captures core concept but could mention statelessness"
}
```

## Tech Stack

- **Frontend:** React, Vite, CSS
- **Backend:** Python, FastAPI, Uvicorn
- **AI/ML:** scikit-learn, TF-IDF, cosine similarity
- **Data:** JSON dataset

## Local Setup

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd interviewsense-ai
```

### 2) Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

### 3) Run frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173`

## Screenshots

Add your app screenshot here after running locally:

- `docs/interviewsense-ui.png`

## Future Improvements

- Add speech-to-text for spoken interview answers.
- Use transformer embeddings (e.g., Sentence-BERT) for semantic scoring.
- Store results per user and show progress dashboards.
- Add role-based question banks (frontend, backend, data science).
- Deploy full stack with Docker and cloud hosting.

## Why this project looks great to recruiters

- Demonstrates full-stack integration (React + FastAPI).
- Includes practical AI evaluation logic with explainable scoring.
- Clean architecture and professional UI.
- Easy to demo and explain in interviews.
