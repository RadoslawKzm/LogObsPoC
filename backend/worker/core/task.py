from loguru import logger
import asyncio



TASK_REGISTRY = {}

def register_task(name):
    def wrapper(func):
        TASK_REGISTRY[name] = func
        return func
    return wrapper

@register_task("process_task")
async def process_task(task: dict):
    """Simulate heavy computation asynchronously."""
    task_id = task.get("task_id")
    document_1 = task.get("document_1")
    document_2 = task.get("document_2")
    logger.info(f"Processing task {task_id}")
    logger.info(f"Comparing documents: {document_1} and {document_2}")
    await asyncio.sleep(5)  # simulate computation without blocking
    logger.info(f"Task {task_id} processed successfully")
    return f"Task {task_id} completed"

@register_task("generate_report")
async def generate_report(task: dict):
    """Simulate heavy computation asynchronously."""
    task_id = task.get("task_id")
    logger.info(f"Processing task {task_id}")
    logger.info(f"Generating report...")
    await asyncio.sleep(30)  # simulate computation without blocking
    logger.info(f"Task {task_id} processed successfully")
    return f"Task {task_id} completed"