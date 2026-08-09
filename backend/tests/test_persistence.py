from pathlib import Path

from app.agent.controller import AgentController
from app.persistence import SQLiteTaskRepository
from app.tools.text_processor import TextProcessorTool


def test_execution_round_trip(tmp_path: Path) -> None:
    repository = SQLiteTaskRepository(tmp_path / "tasks.sqlite3")
    repository.initialize()
    execution = AgentController([TextProcessorTool()]).execute("uppercase: hello")

    saved = repository.save_execution("uppercase: hello", execution)
    records = repository.list_recent_executions()

    assert records == [saved]
    assert saved.id == 1
    assert saved.task == "uppercase: hello"
    assert saved.output == "HELLO"
    assert saved.tools_used == ("text_processor",)
    assert saved.trace == execution.trace
    assert saved.timestamp == execution.timestamp

