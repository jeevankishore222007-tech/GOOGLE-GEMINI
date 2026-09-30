import json
from pydantic import BaseModel, Field
from gemini_client import generate_json


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)


QUIZ_SCHEMA = QuizResponse.model_json_schema()


def generate_quiz(text: str) -> list[dict]:
    text = text.strip()
    if not text:
        raise ValueError("Please provide a topic or passage for the quiz.")

    prompt = f"""
Create exactly 3 multiple-choice questions for an educational quiz.

Source topic/passage:
{text}

Requirements:
- Exactly 3 questions.
- Exactly 4 options per question.
- Exactly one correct answer per question.
- The "answer" field must exactly match one option.
- Questions must test understanding, not just trivial word matching.
- Keep the wording suitable for students.
- Return only JSON matching the supplied schema.
"""
    try:
        raw = generate_json(prompt, QUIZ_SCHEMA)
        parsed = QuizResponse.model_validate(json.loads(raw))
        return [question.model_dump() for question in parsed.questions]
    except Exception as exc:
        raise RuntimeError(f"Quiz generation failed: {exc}") from exc
