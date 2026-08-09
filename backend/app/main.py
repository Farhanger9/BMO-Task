import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.agent.controller import AgentController
from app.api import create_task_router
from app.persistence import SQLiteTaskRepository
from app.tools.calculator import CalculatorTool
from app.tools.text_processor import TextProcessorTool
from app.tools.weather_mock import WeatherMockTool


def create_app(database_path: str | Path | None = None) -> FastAPI:
    resolved_database_path = database_path or os.getenv(
        "TASK_DATABASE_PATH", "tasks.sqlite3"
    )
    repository = SQLiteTaskRepository(resolved_database_path)
    controller = AgentController(
        [TextProcessorTool(), CalculatorTool(), WeatherMockTool()]
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        repository.initialize()
        yield

    application = FastAPI(title="Agent task API", lifespan=lifespan)
    application.include_router(create_task_router(controller, repository))
    return application


app = create_app()
