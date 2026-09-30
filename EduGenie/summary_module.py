from gemini_client import generate_text


def summarize_text(text: str) -> str:
    text = text.strip()
    if not text:
        raise ValueError("Please provide text to summarize.")

    prompt = f"""
Summarize the following educational passage for quick revision.

Requirements:
- Preserve the important facts and relationships.
- Remove repetition and unnecessary detail.
- Use simple, clear language.
- Prefer a short introductory sentence followed by bullets when appropriate.
- Do not add facts that are absent from the passage.

PASSAGE:
{text}
"""
    try:
        return generate_text(prompt)
    except Exception as exc:
        raise RuntimeError(f"Summary generation failed: {exc}") from exc
