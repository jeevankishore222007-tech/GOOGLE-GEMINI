from quiz_module import QuizResponse


def test_quiz_schema_accepts_three_questions():
    data = {
        "questions": [
            {"question": "Q1", "options": ["A", "B", "C", "D"], "answer": "A"},
            {"question": "Q2", "options": ["A", "B", "C", "D"], "answer": "B"},
            {"question": "Q3", "options": ["A", "B", "C", "D"], "answer": "C"},
        ]
    }
    result = QuizResponse.model_validate(data)
    assert len(result.questions) == 3
    assert all(len(q.options) == 4 for q in result.questions)
