from collections.abc import Sequence
from datetime import UTC, datetime

from app.agent.models import AgentExecutionResult, ExecutionTraceEntry
from app.tools.tool import Tool


class AgentController:
    def __init__(self, tools: Sequence[Tool]) -> None:
        self._tools = tuple(tools)

    def execute(self, task: str) -> AgentExecutionResult:
        trace = [
            ExecutionTraceEntry(stage="received", message="Task received."),
        ]

        for tool in self._tools:
            if not tool.can_handle(task):
                continue

            trace.append(
                ExecutionTraceEntry(
                    stage="selected",
                    message=f"Selected {tool.name}.",
                    tool=tool.name,
                )
            )
            result = tool.execute(task)
            trace.append(
                ExecutionTraceEntry(
                    stage="executed",
                    message=f"Tool execution {result.status}.",
                    tool=tool.name,
                )
            )
            return AgentExecutionResult(
                status=result.status,
                output=result.output,
                tools_used=(tool.name,),
                trace=tuple(trace),
                timestamp=datetime.now(UTC),
            )

        trace.append(
            ExecutionTraceEntry(
                stage="unsupported",
                message="No tool could handle the task.",
            )
        )
        return AgentExecutionResult(
            status="error",
            output="Unsupported task.",
            tools_used=(),
            trace=tuple(trace),
            timestamp=datetime.now(UTC),
        )

