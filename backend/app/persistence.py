import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol

from app.agent.models import AgentExecutionResult, ExecutionTraceEntry


@dataclass(frozen=True)
class StoredTaskExecution:
    id: int
    task: str
    output: str
    tools_used: tuple[str, ...]
    trace: tuple[ExecutionTraceEntry, ...]
    timestamp: datetime


class TaskRepository(Protocol):
    def save_execution(
        self, task: str, execution: AgentExecutionResult
    ) -> StoredTaskExecution: ...

    def list_recent_executions(self) -> list[StoredTaskExecution]: ...


class SQLiteTaskRepository:
    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)

    def initialize(self) -> None:
        with sqlite3.connect(self._database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS task_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    output TEXT NOT NULL,
                    tools_used_json TEXT NOT NULL,
                    trace_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )

    def save_execution(
        self, task: str, execution: AgentExecutionResult
    ) -> StoredTaskExecution:
        tools_used_json = json.dumps(execution.tools_used)
        trace_json = json.dumps([asdict(entry) for entry in execution.trace])
        timestamp = execution.timestamp.isoformat()

        with sqlite3.connect(self._database_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO task_executions (
                    task,
                    output,
                    tools_used_json,
                    trace_json,
                    timestamp
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (task, execution.output, tools_used_json, trace_json, timestamp),
            )
            execution_id = cursor.lastrowid

        if execution_id is None:
            raise sqlite3.DatabaseError("SQLite did not return an execution id")

        return StoredTaskExecution(
            id=execution_id,
            task=task,
            output=execution.output,
            tools_used=execution.tools_used,
            trace=execution.trace,
            timestamp=execution.timestamp,
        )

    def list_recent_executions(self) -> list[StoredTaskExecution]:
        with sqlite3.connect(self._database_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT id, task, output, tools_used_json, trace_json, timestamp
                FROM task_executions
                ORDER BY timestamp DESC, id DESC
                """
            ).fetchall()

        return [self._record_from_row(row) for row in rows]

    @staticmethod
    def _record_from_row(row: sqlite3.Row) -> StoredTaskExecution:
        trace_data = json.loads(row["trace_json"])
        return StoredTaskExecution(
            id=row["id"],
            task=row["task"],
            output=row["output"],
            tools_used=tuple(json.loads(row["tools_used_json"])),
            trace=tuple(ExecutionTraceEntry(**entry) for entry in trace_data),
            timestamp=datetime.fromisoformat(row["timestamp"]),
        )

