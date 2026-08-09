from fastapi import APIRouter, status

from app.agent.controller import AgentController
from app.api_models import TaskRequest, TaskResponse
from app.persistence import TaskRepository


def create_task_router(
    controller: AgentController, repository: TaskRepository
) -> APIRouter:
    router = APIRouter(prefix="/api/tasks", tags=["tasks"])

    @router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
    def execute_task(request: TaskRequest) -> TaskResponse:
        execution = controller.execute(request.task)
        record = repository.save_execution(request.task, execution)
        return TaskResponse.from_record(record)

    @router.get("", response_model=list[TaskResponse])
    def list_tasks() -> list[TaskResponse]:
        return [
            TaskResponse.from_record(record)
            for record in repository.list_recent_executions()
        ]

    return router

