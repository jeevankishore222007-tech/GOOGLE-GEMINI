# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript learning assistant based on the supplied project documentation.

## Features

- Question answering: `POST /qa`
- Concept explanation: `POST /explain`
- Three-question MCQ quiz generation: `POST /quiz`
- Passage summarization: `POST /summarize`
- Beginner-to-advanced learning path: `POST /learn/recommendations`
- Browser UI served directly by FastAPI
- Optional local LaMini-Flan-T5-783M explanation backend
- Gemini structured JSON output for quiz generation
- Health endpoint: `GET /health`

## Architecture

```text
Browser
   |
   v
FastAPI (main.py)
   |
   +--> qna.py ----------------------> Gemini
   +--> explanation_module.py -------> Gemini OR local LaMini-Flan-T5
   +--> quiz_module.py --------------> Gemini (structured JSON)
   +--> summary_module.py -----------> Gemini
   +--> learning_path.py ------------> Gemini
```

## Why the model setting is configurable

The supplied documentation specifies Gemini 1.5 Pro. Model availability changes over time, so this implementation uses the current Gemini SDK and makes the model configurable through `GEMINI_MODEL`. The default can be changed without editing Python code.

## VS Code setup

### 1. Open the project

Open this folder in VS Code:

```text
EduGenie/
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Then put your Gemini API key in `.env`:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
```

### 5. Start the server

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Testing

### Browser test

Try:

1. Question: `Which is the largest ocean?`
2. Explanation: `Pythagoras theorem`
3. Summary: paste a paragraph.
4. Quiz: `Pythagoras theorem`
5. Learning path: `SQL`

For the quiz, select an option and click **Check Answer**.

### API health test

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"ok","service":"EduGenie"}
```

### API question test

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"What is photosynthesis?\"}"
```

On macOS/Linux use:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"text":"What is photosynthesis?"}'
```

## Optional local LaMini explanation model

The project documentation describes LaMini-Flan-T5-783M for explanations. To use it:

```bash
pip install -r requirements-local.txt
```

Then change `.env`:

```env
EXPLANATION_BACKEND=local
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The first local explanation may take longer because the model must be downloaded and loaded.

## Troubleshooting

### "GEMINI_API_KEY is not configured"

Make sure `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart Uvicorn after changing `.env`.

### Gemini model error

Set a model that is available to your API account, for example:

```env
GEMINI_MODEL=gemini-2.5-flash
```

The application does not hard-code the model in individual modules.

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    └── style.css
```
