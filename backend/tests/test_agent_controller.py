from app.agent.controller import AgentController
from app.agent.models import ToolExecutionResult
from app.tools.calculator import CalculatorTool
from app.tools.text_processor import TextProcessorTool
from app.tools.weather_mock import WeatherMockTool


class _AlwaysMatchingTool:
    name = "first_match"

    def can_handle(self, task: str) -> bool:
        return True

    def execute(self, task: str) -> ToolExecutionResult:
        return ToolExecutionResult(status="success", output="handled first")


def test_controller_selects_first_appropriate_tool() -> None:
    controller = AgentController(
        [_AlwaysMatchingTool(), TextProcessorTool(), CalculatorTool()]
    )

    result = controller.execute("uppercase: hello")

    assert result.status == "success"
    assert result.output == "handled first"
    assert result.tools_used == ("first_match",)
    assert [entry.stage for entry in result.trace] == [
        "received",
        "selected",
        "executed",
    ]


def test_controller_routes_tasks_to_the_matching_tool() -> None:
    controller = AgentController(
        [TextProcessorTool(), CalculatorTool(), WeatherMockTool()]
    )

    result = controller.execute("6 * 7")

    assert result.output == "42"
    assert result.tools_used == ("calculator",)


def test_controller_returns_a_predictable_unsupported_result() -> None:
    controller = AgentController(
        [TextProcessorTool(), CalculatorTool(), WeatherMockTool()]
    )

    result = controller.execute("Tell me a joke")

    assert result.status == "error"
    assert result.output == "Unsupported task."
    assert result.tools_used == ()
    assert result.trace[-1].stage == "unsupported"

