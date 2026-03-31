from celery import Celery
from app.core.config import settings
import logging
import time

logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.workers.task_scheduler.process_agent_task": "main-queue"
}

@celery_app.task
def process_agent_task(task_type: str, payload: dict):
    """
    Background worker handles async jobs:
    - job scraping + alerts
    - study reminders
    - business insights generation
    """
    logger.info(f"Executing async task: {task_type}")
    # Simulating long-running job processing
    time.sleep(2) 
    
    if task_type == "job_scraping":
        logger.info(f"Scraped jobs for user {payload.get('user_id')}")
    elif task_type == "study_reminder":
        logger.info(f"Processed study reminders for {payload.get('user_id')}")
    elif task_type == "business_insights":
        logger.info(f"Generated business report based on payload: {payload}")
    else:
        logger.warning(f"Unknown task type: {task_type}")
        
    return {"status": "completed", "task_type": task_type}
