import aio_pika
from loguru import logger
from pydantic_settings import BaseSettings


async def init_rabbit(*, settings: BaseSettings):
    """
    Create an async RabbitMQ connection and channel.
    """
    logger.info("Connecting to RabbitMQ...")
    # Build AMQP URL
    user = settings.RABBITMQ_USER
    password = settings.RABBITMQ_PASSWORD or ""
    host = settings.RABBITMQ_HOST
    port = settings.RABBITMQ_PORT
    vhost = settings.RABBITMQ_VIRTUAL_HOST
    amqp_url = f"amqp://{user}:{password}@{host}:{port}/{vhost}"
    # Connect
    connection = await aio_pika.connect_robust(amqp_url, heartbeat=30)
    channel = await connection.channel()
    logger.info("Connected to RabbitMQ!")
    return connection, channel


async def declare_queues(*, channel, settings: BaseSettings):
    # Declare queue (idempotent)
    logger.info("Declaring RabbitMQ queues...")
    await channel.declare_queue(settings.RABBITMQ_S_QUEUE, durable=True)
    logger.info(f"RabbitMQ {settings.RABBITMQ_S_QUEUE} declared!")
    await channel.declare_queue(settings.RABBITMQ_M_QUEUE, durable=True)
    logger.info(f"RabbitMQ {settings.RABBITMQ_M_QUEUE} declared!")
    await channel.declare_queue(settings.RABBITMQ_L_QUEUE, durable=True)
    logger.info(f"RabbitMQ {settings.RABBITMQ_L_QUEUE} declared!")
    logger.info("RabbitMQ queues declared!")
