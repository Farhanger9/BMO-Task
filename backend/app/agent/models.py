from dataclasses import dataclass
from datetime import datetime
from typing import Literal

ExecutionStatus = Literal["success", "error"]
TraceStage = Literal["received", "selected", "executed", "unsupported"]


@dataclass(frozen=True)
class ToolExecutionResult:
    status: ExecutionStatus
    output: str


@dataclass(frozen=True)
class ExecutionTraceEntry:
    stage: TraceStage
    message: str
    tool: str | None = None


@dataclass(frozen=True)
class AgentExecutionResult:
    status: ExecutionStatus
    output: str
    tools_used: tuple[str, ...]
    trace: tuple[ExecutionTraceEntry, ...]
    timestamp: datetime

