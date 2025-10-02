from .task import process_task, TASK_REGISTRY
import json
from loguru import logger
import aio_pika
from backend.worker.config import worker_settings


async def callback(message: aio_pika.IncomingMessage):
    """RabbitMQ message callback (async)."""

    corr_id = message.correlation_id or "No correlation_id"
    # Push correlation_id to Loguru context
    task_obj = TASK_REGISTRY.get(message.type, None)
    if not task_obj:
        raise ValueError(f"Task:`{message.type}` not registered.")
    with logger.contextualize(correlation_id=corr_id):
        async with message.process():  # automatically ack/nack
            try:
                task = json.loads(message.body)
                logger.info(f"Task received: {task}")
                logger.info(f"Dispatching task {task_obj}: {task}")
                await task_obj(task)
            except Exception as e:
                logger.error(f"Error processing task: {str(e)}", exc_info=True)
                # Message will be requeued automatically if exception occurs


async def rabbit_worker(
    connection: aio_pika.RobustConnection,
    queue_name: str = worker_settings.WORKER_RABBIT_QUEUE,
):
    """Start async RabbitMQ worker."""
    channel = await connection.channel()
    await channel.set_qos(
        prefetch_count=worker_settings.RABBITMQ_PREFETCH_COUNT
    )
    queue = await channel.get_queue(queue_name)
    # queue = await channel.declare_queue(queue_name, durable=True)
    logger.info("Worker is waiting for tasks...")
    await queue.consume(callback)
