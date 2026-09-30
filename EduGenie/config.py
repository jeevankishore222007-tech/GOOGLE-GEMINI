import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# The documentation used Gemini 1.5 Pro. The current implementation keeps
# the model configurable because Gemini model availability changes over time.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

# "gemini" is the reliable default. Set to "local" to use LaMini-Flan-T5-783M.
EXPLANATION_BACKEND = os.getenv("EXPLANATION_BACKEND", "gemini").strip().lower()
LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M",
).strip()

MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))
