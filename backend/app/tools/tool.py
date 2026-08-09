from typing import Protocol

from app.agent.models import ToolExecutionResult


class Tool(Protocol):
    name: str

    def can_handle(self, task: str) -> bool: ...

    def execute(self, task: str) -> ToolExecutionResult: ...

