from loguru import logger
import aio_pika
from pydantic_settings import BaseSettings


async def init_rabbit(*, settings: BaseSettings):
    """
    Create an async RabbitMQ connection and channel; declare queue and return both.
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


# from loguru import logger
# import aio_pika
# from backend.database.config import rabbit_config
#
#
# def init_rabbit():
#     """Create a RabbitMQ connection and channel; declare topology and return both."""
#     logger.info("Connecting to RabbitMQ...")
#     credentials = pika.PlainCredentials(
#         rabbit_config.RABBITMQ_USER,
#         rabbit_config.RABBITMQ_PASSWORD or "",
#     )
#     parameters = pika.ConnectionParameters(
#         host=rabbit_config.RABBITMQ_HOST,
#         port=rabbit_config.RABBITMQ_PORT,
#         virtual_host=rabbit_config.RABBITMQ_VIRTUAL_HOST,
#         credentials=credentials,
#         heartbeat=30,
#         blocked_connection_timeout=120,
#         connection_attempts=5,
#         retry_delay=2,
#     )
#     connection = pika.BlockingConnection(parameters)
#     channel = connection.channel()
#
#     # Ensure queue exists (idempotent)
#     channel.queue_declare(queue=rabbit_config.RABBITMQ_QUEUE, durable=True)
#
#     # If you use an exchange and routing key, ensure they exist and are bound.
#     # Uncomment and adjust exchange_type if you publish via exchanges.
#     # channel.exchange_declare(
#     #     exchange=worker_settings.RABBITMQ_EXCHANGE, exchange_type="direct", durable=True
#     # )
#     # channel.queue_bind(
#     #     queue=worker_settings.RABBITMQ_QUEUE,
#     #     exchange=worker_settings.RABBITMQ_EXCHANGE,
#     #     routing_key=worker_settings.RABBITMQ_ROUTING_KEY,
#     # )
#     logger.info("Connected to RabbitMQ!")
#     return connection, channel
