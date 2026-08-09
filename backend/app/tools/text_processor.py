from dataclasses import dataclass
from typing import Literal

from app.agent.models import ToolExecutionResult

TextOperation = Literal["uppercase", "lowercase", "word_count"]


@dataclass(frozen=True)
class _TextRequest:
    operation: TextOperation
    text: str


class TextProcessorTool:
    name = "text_processor"

    _operations: tuple[tuple[str, TextOperation], ...] = (
        ("uppercase", "uppercase"),
        ("lowercase", "lowercase"),
        ("word count", "word_count"),
    )

    def can_handle(self, task: str) -> bool:
        normalized = task.strip().lower()
        return any(
            normalized == label
            or normalized.startswith(f"{label}:")
            or normalized.startswith(f"{label} ")
            for label, _ in self._operations
        )

    def execute(self, task: str) -> ToolExecutionResult:
        parsed = self._parse(task)
        if isinstance(parsed, ToolExecutionResult):
            return parsed

        if parsed.operation == "uppercase":
            output = parsed.text.upper()
        elif parsed.operation == "lowercase":
            output = parsed.text.lower()
        else:
            output = str(len(parsed.text.split()))

        return ToolExecutionResult(status="success", output=output)

    def _parse(self, task: str) -> _TextRequest | ToolExecutionResult:
        stripped = task.strip()
        normalized = stripped.lower()

        command_text = normalized.split(":", maxsplit=1)[0]
        mentioned_operations = [
            label for label, _ in self._operations if label in command_text
        ]
        if len(mentioned_operations) > 1:
            return ToolExecutionResult(
                status="error",
                output="Ambiguous text operation. Choose only one operation.",
            )

        for label, operation in self._operations:
            if normalized == label:
                text = ""
            elif normalized.startswith(f"{label}:"):
                text = stripped[len(label) + 1 :].strip()
            elif normalized.startswith(f"{label} "):
                text = stripped[len(label) :].strip()
            else:
                continue

            if not text:
                return ToolExecutionResult(
                    status="error",
                    output=f"Missing text for {label}.",
                )
            return _TextRequest(operation=operation, text=text)

        return ToolExecutionResult(
            status="error",
            output="Unsupported text operation. Use uppercase, lowercase, or word count.",
        )

