from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Please provide a topic.")

    prompt = f"""
You are EduGenie, a personalized learning-path designer.

Create a structured learning path for: {topic}

Include:
1. Beginner level: foundations and an estimated time.
2. Intermediate level: concepts and practice.
3. Advanced level: deeper topics and projects.
4. Useful resource types or example resources to look for.
5. Practice suggestions.
6. Adaptive learning tips for someone who wants to go faster or slower.

Keep the plan practical and readable. Do not claim that a specific external resource was checked live.
"""
    try:
        return generate_text(prompt)
    except Exception as exc:
        raise RuntimeError(f"Learning-path generation failed: {exc}") from exc
