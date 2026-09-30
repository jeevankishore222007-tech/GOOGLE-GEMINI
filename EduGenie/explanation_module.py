from config import EXPLANATION_BACKEND, LOCAL_EXPLANATION_MODEL
from gemini_client import generate_text


_LOCAL_PIPELINE = None


def _get_local_pipeline():
    global _LOCAL_PIPELINE
    if _LOCAL_PIPELINE is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
        except ImportError as exc:
            raise RuntimeError(
                "Local explanation mode requires transformers and torch. "
                "Install requirements-local.txt or switch EXPLANATION_BACKEND=gemini."
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(LOCAL_EXPLANATION_MODEL)
        model = AutoModelForSeq2SeqLM.from_pretrained(LOCAL_EXPLANATION_MODEL)
        _LOCAL_PIPELINE = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
        )
    return _LOCAL_PIPELINE


def _explain_with_local_model(topic: str) -> str:
    generator = _get_local_pipeline()
    prompt = (
        f"Explain the concept of '{topic}' in simple language for a school student. "
        "Use short paragraphs and one simple example."
    )
    result = generator(
        prompt,
        max_new_tokens=180,
        do_sample=True,
        temperature=0.7,
    )
    return result[0]["generated_text"].strip()


def _explain_with_gemini(topic: str) -> str:
    prompt = f"""
You are EduGenie, an educational tutor.

Explain "{topic}" for a learner who may be new to the subject.
Requirements:
- Start with a one-sentence definition.
- Explain the idea in simple language.
- Use 3 to 5 short bullet points when useful.
- Give one concrete example.
- Avoid unnecessary jargon.
- If the topic is ambiguous, state the interpretation you are using.
"""
    return generate_text(prompt)


def explain_topic(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic.")

    try:
        if EXPLANATION_BACKEND == "local":
            return _explain_with_local_model(topic)
        return _explain_with_gemini(topic)
    except Exception as exc:
        # Keep the API readable for users while preserving the actual cause.
        raise RuntimeError(f"Explanation generation failed: {exc}") from exc
