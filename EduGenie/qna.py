from gemini_client import generate_text


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Please provide a question.")

    prompt = f"""
You are EduGenie, a concise educational Q&A assistant.

Answer the student's question:
{question}

Rules:
- Give a direct answer first.
- Then add brief context if useful.
- Prefer simple, accurate language.
- Use a small example when it improves understanding.
- If the question depends on missing context, say what assumption you made.
- Do not invent sources or citations.
"""
    try:
        return generate_text(prompt)
    except Exception as exc:
        raise RuntimeError(f"Q&A generation failed: {exc}") from exc
