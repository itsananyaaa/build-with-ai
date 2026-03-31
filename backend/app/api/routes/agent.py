from fastapi import APIRouter, Depends
from app.models.schemas import AgentTaskRequest
from app.workers.task_scheduler import process_agent_task
from app.core.security import get_current_user

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/run-task")
async def run_agent_task(request: AgentTaskRequest, current_user: dict = Depends(get_current_user)):
    """
    Submits a background task to the celery worker using the Queue-based architecture.
    Handles scheduling of 'job_scraping', 'study_reminder', and 'business_insights'.
    """
    # Incorporate user authentication / user_id securely directly inside payload
    payload = request.payload.copy()
    payload["user_id"] = current_user["user_id"]

    try:
        # Trigger celery async task delay
        task_id = process_agent_task.delay(request.task_type, payload)
        return {"status": "success", "message": "Task appended to queue", "task_id": str(task_id)}
    except Exception as e:
        # Fallback local testing if celery running isn't active
        return {"status": "failed", "message": f"Queue failed: {str(e)}"}
