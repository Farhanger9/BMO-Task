from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.agent.models import ExecutionTraceEntry
from app.persistence import StoredTaskExecution


class TaskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    task: str = Field(min_length=1)


class TaskResponse(BaseModel):
    id: int
    task: str
    output: str
    tools_used: tuple[str, ...]
    trace: tuple[ExecutionTraceEntry, ...]
    timestamp: datetime

    @classmethod
    def from_record(cls, record: StoredTaskExecution) -> "TaskResponse":
        return cls(
            id=record.id,
            task=record.task,
            output=record.output,
            tools_used=record.tools_used,
            trace=record.trace,
            timestamp=record.timestamp,
        )

