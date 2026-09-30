from functools import lru_cache
from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be used because configuration is missing."""


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env and add your API key."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str, *, temperature: float | None = None, max_output_tokens: int | None = None) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE if temperature is None else temperature,
            max_output_tokens=MAX_OUTPUT_TOKENS if max_output_tokens is None else max_output_tokens,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def generate_json(prompt: str, schema: dict) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text.strip()
