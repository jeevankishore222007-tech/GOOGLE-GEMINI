from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="A lightweight educational assistant with Q&A, explanations, quizzes, summaries and learning paths.",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class TopicRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(request: TextRequest):
    return {"question": request.text, "answer": answer_question(request.text)}


@app.get("/qa")
async def qa_get(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Please provide a question.")
    return {"question": question, "answer": answer_question(question)}


@app.post("/explain")
async def explain(request: TopicRequest):
    return {"topic": request.topic, "explanation": explain_topic(request.topic)}


@app.post("/quiz")
async def quiz(request: TextRequest):
    return {"quiz": generate_quiz(request.text)}


@app.post("/summarize")
async def summarize(request: TextRequest):
    return {"text": request.text, "summary": summarize_text(request.text)}


@app.post("/learn/recommendations")
async def recommendations(request: TopicRequest):
    return {
        "topic": request.topic,
        "recommendation": get_learning_recommendations(request.topic),
    }


@app.get("/learn/recommendations")
async def recommendations_get(topic: str):
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Please provide a topic.")
    return {
        "topic": topic,
        "recommendation": get_learning_recommendations(topic),
    }
