def test_project_modules_import():
    import config
    import gemini_client
    import explanation_module
    import qna
    import quiz_module
    import summary_module
    import learning_path
    import main

    assert main.app.title.startswith("EduGenie")
