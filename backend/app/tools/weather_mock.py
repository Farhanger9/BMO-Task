from dataclasses import dataclass

from app.agent.models import ToolExecutionResult


@dataclass(frozen=True)
class _MockWeather:
    temperature_celsius: int
    conditions: str


class WeatherMockTool:
    name = "weather_mock"

    _weather_by_city = {
        "toronto": _MockWeather(18, "partly cloudy"),
        "vancouver": _MockWeather(14, "rain"),
        "montreal": _MockWeather(20, "sunny"),
    }
    _default_weather = _MockWeather(22, "clear")
    _city_markers = ("weather in ", "weather for ")

    def can_handle(self, task: str) -> bool:
        return "weather" in task.lower().split()

    def execute(self, task: str) -> ToolExecutionResult:
        city = self._extract_city(task)
        if city is None:
            return ToolExecutionResult(
                status="error",
                output="Please specify a city using 'weather in <city>'.",
            )

        weather = self._weather_by_city.get(city.lower(), self._default_weather)
        output = (
            f"Weather for {city}: {weather.temperature_celsius}°C, "
            f"{weather.conditions}."
        )
        return ToolExecutionResult(status="success", output=output)

    def _extract_city(self, task: str) -> str | None:
        normalized = task.lower()
        for marker in self._city_markers:
            marker_index = normalized.find(marker)
            if marker_index == -1:
                continue

            city_start = marker_index + len(marker)
            city = task[city_start:].strip(" ?!.")
            return city.title() if city else None

        return None

