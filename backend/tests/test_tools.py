import pytest

from app.tools.calculator import CalculatorTool
from app.tools.text_processor import TextProcessorTool
from app.tools.weather_mock import WeatherMockTool


@pytest.mark.parametrize(
    ("task", "expected_output"),
    [
        ("uppercase: Hello there", "HELLO THERE"),
        ("lowercase: Hello THERE", "hello there"),
        ("word count: one two three", "3"),
    ],
)
def test_text_operations(task: str, expected_output: str) -> None:
    result = TextProcessorTool().execute(task)

    assert result.status == "success"
    assert result.output == expected_output


@pytest.mark.parametrize(
    ("task", "expected_output"),
    [
        ("2 + 3", "5"),
        ("calculate: 7 - 10", "-3"),
        ("4 * 2.5", "10"),
        ("9 / 4", "2.25"),
    ],
)
def test_arithmetic(task: str, expected_output: str) -> None:
    result = CalculatorTool().execute(task)

    assert result.status == "success"
    assert result.output == expected_output


def test_divide_by_zero_is_an_error() -> None:
    result = CalculatorTool().execute("10 / 0")

    assert result.status == "error"
    assert result.output == "Cannot divide by zero."


def test_weather_uses_deterministic_mock_data() -> None:
    result = WeatherMockTool().execute("What is the weather in Toronto?")

    assert result.status == "success"
    assert result.output == "Weather for Toronto: 18°C, partly cloudy."

