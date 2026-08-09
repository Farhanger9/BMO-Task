from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    app = create_app(tmp_path / "tasks.sqlite3")
    with TestClient(app) as test_client:
        yield test_client


def test_post_task_success(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"task": "uppercase: hello"})

    assert response.status_code == 201
    response_body = response.json()
    timestamp = datetime.fromisoformat(response_body.pop("timestamp"))
    assert timestamp.tzinfo is not None
    assert response_body == {
        "id": 1,
        "task": "uppercase: hello",
        "output": "HELLO",
        "tools_used": ["text_processor"],
        "trace": [
            {"stage": "received", "message": "Task received.", "tool": None},
            {
                "stage": "selected",
                "message": "Selected text_processor.",
                "tool": "text_processor",
            },
            {
                "stage": "executed",
                "message": "Tool execution success.",
                "tool": "text_processor",
            },
        ],
    }


def test_get_task_history_returns_most_recent_first(client: TestClient) -> None:
    client.post("/api/tasks", json={"task": "uppercase: first"})
    client.post("/api/tasks", json={"task": "lowercase: SECOND"})

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert [record["task"] for record in response.json()] == [
        "lowercase: SECOND",
        "uppercase: first",
    ]


def test_unsupported_task_is_persisted_as_a_completed_execution(
    client: TestClient,
) -> None:
    response = client.post("/api/tasks", json={"task": "Tell me a joke"})

    assert response.status_code == 201
    assert response.json()["output"] == "Unsupported task."
    assert response.json()["tools_used"] == []
    assert response.json()["trace"][-1]["stage"] == "unsupported"

    history = client.get("/api/tasks").json()
    assert history == [response.json()]


def test_empty_task_is_rejected(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"task": "   "})

    assert response.status_code == 422
    assert client.get("/api/tasks").json() == []
