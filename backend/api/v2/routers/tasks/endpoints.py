import json

import aio_pika
import fastapi
import pydantic
from asgi_correlation_id import correlation_id
from loguru import logger

from backend.api.config import settings

from . import examples

tasks_router = fastapi.APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(pydantic.BaseModel):
    user: str = pydantic.Field(..., examples=["alice", "bob"])


@tasks_router.post(
    "/",
    status_code=200,
    responses=examples.response.success,
)
async def create_task(
    payload: TaskCreate,
    request: fastapi.Request,
) -> fastapi.responses.JSONResponse:
    rabbit_ch = request.app.state.rabbit_channel
    logger.debug(f"Create task called with user={payload.user}")
    # Prepare a fake task
    task_message = {
        "task_id": "example-task-id",
        "user": payload.user,
        "status": "created",
    }
    message_body = json.dumps(task_message).encode()

    # Publish a message to a queue named "tasks"
    await rabbit_ch.default_exchange.publish(
        aio_pika.Message(
            body=message_body,
            correlation_id=correlation_id.get(),
            type="generate_report",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=settings.RABBITMQ_S_QUEUE,
    )
    logger.info(
        f"Published dummy task to RabbitMQ. " f"Queue 'tasks': {task_message}"
    )

    return fastapi.responses.JSONResponse(
        content={"data": task_message},
        status_code=fastapi.status.HTTP_200_OK,
    )


@tasks_router.get(
    "/{task_id}",
    status_code=200,
    responses=examples.response.success,
)
async def get_tasks(task_id: str) -> fastapi.responses.JSONResponse:
    logger.debug(f"Get task called for task_id={task_id}")
    return fastapi.responses.JSONResponse(
        content={"data": {"task_id": task_id, "status": "pending"}},
        status_code=fastapi.status.HTTP_200_OK,
    )
