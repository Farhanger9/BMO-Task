# Agent Task Runner

## Overview

Agent Task Runner is a small full-stack application with a React and TypeScript frontend, a FastAPI backend, and SQLite task history. A deterministic `AgentController` routes each request to one of three predefined tools—text processing, calculation, or mock weather—and returns a structured execution trace with the result.

## Architecture

```text
React frontend
    → FastAPI
    → AgentController
    → selected Tool
    → SQLite persistence
    → structured response
```

Routing is deliberately rule-based rather than LLM-driven, which keeps supported behavior deterministic and testable. The `Tool` protocol contains only routing and execution methods; SQLite uses Python's built-in `sqlite3`, with tool names and trace events stored as readable JSON.

The backend remains synchronous because every operation is local and blocking at this scale. The frontend uses local React state, and the project avoids service layers, ORMs, state frameworks, and other abstractions that do not earn their cost here.

## Requirements

- Python 3.11 or newer; tested with Python 3.13.11
- Node.js `^20.19.0` or `>=22.12.0`; tested with Node.js 25.2.1
- npm; tested with npm 11.6.2

The final validation used FastAPI 0.141.1, Uvicorn 0.52.1, pytest 8.4.2, React 19.2.8, TypeScript 5.9.3, and Vite 7.3.6. Supported dependency ranges are declared in `backend/pyproject.toml` and locked for the frontend in `frontend/package-lock.json`.

## Backend setup

From a fresh clone on macOS or Linux:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead.

## Frontend setup

In a separate terminal from the repository root:

```bash
cd frontend
npm ci
```

## Running the application

Start the backend in the first terminal:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Start the frontend in the second terminal:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` requests to FastAPI at `http://127.0.0.1:8000`. The backend creates `backend/tasks.sqlite3` automatically on startup unless `TASK_DATABASE_PATH` specifies another path.

## Example tasks

```text
uppercase: deployment ready
lowercase: RELEASE NOTES
word count: one two three
calculate: 9 / 4
weather in Toronto
```

The calculator prefix is optional, so `12 + 8` also works.

## Testing

Run the backend tests from the repository root after backend setup:

```bash
cd backend
.venv/bin/python -m pytest -q
```

Run the frontend type-check and production build after frontend setup:

```bash
cd frontend
npm run build
```

## Assumptions and tradeoffs

- Tool routing is deterministic and supports only the predefined request formats.
- The calculator accepts two numeric operands and one of `+`, `-`, `*`, or `/`; it does not support parentheses or chained expressions.
- Weather data is deterministic mock data and does not call an external service.
- Task history is currently unbounded.
- JSON trace storage is readable but is not designed for SQL analytics.
- Production deployment and reverse-proxy configuration are outside this challenge's scope.

## Time spent

Approximately [fill in] hours of focused implementation and review.

## With more time

- Add a simple limit or pagination for task history.
- Add broader integration and browser-level end-to-end tests.
- Define stronger production deployment and reverse-proxy configuration.
- Consider multi-step tool execution if a concrete workflow requires it.
