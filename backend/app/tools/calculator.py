import re

from app.agent.models import ToolExecutionResult


class CalculatorTool:
    name = "calculator"

    _expression_pattern = re.compile(
        r"^(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)$"
    )

    def can_handle(self, task: str) -> bool:
        expression = task.strip()
        normalized = expression.lower()
        return normalized == "calculate" or normalized.startswith(
            ("calculate ", "calculate:")
        ) or self._expression_pattern.fullmatch(expression) is not None

    def execute(self, task: str) -> ToolExecutionResult:
        expression = self._remove_command(task.strip())
        match = self._expression_pattern.fullmatch(expression)
        if match is None:
            return ToolExecutionResult(
                status="error",
                output="Malformed calculation. Use: <number> <+|-|*|/> <number>.",
            )

        left_text, operator, right_text = match.groups()
        left = float(left_text)
        right = float(right_text)

        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        else:
            if right == 0:
                return ToolExecutionResult(
                    status="error",
                    output="Cannot divide by zero.",
                )
            result = left / right

        return ToolExecutionResult(status="success", output=self._format_number(result))

    @staticmethod
    def _remove_command(task: str) -> str:
        normalized = task.lower()
        if normalized.startswith("calculate:"):
            return task[len("calculate:") :].strip()
        if normalized.startswith("calculate "):
            return task[len("calculate ") :].strip()
        if normalized == "calculate":
            return ""
        return task

    @staticmethod
    def _format_number(value: float) -> str:
        if value.is_integer():
            return str(int(value))
        return format(value, ".12g")

