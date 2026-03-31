from fastapi import APIRouter, Depends
from app.models.schemas import MemoryContextResponse
from app.services.memory_system import memory_system
from app.services.persona_manager import PersonaManager
from app.core.security import get_current_user

router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("/context", response_model=MemoryContextResponse)
async def get_memory_context(limit: int = 5, current_user: dict = Depends(get_current_user)):
    """
    Retrieves isolated, role-based vector memory context based on active persona.
    Ensures strict data isolation. No cross-user or cross-persona leakage.
    """
    user_id = current_user["user_id"]
    active_persona_profile = PersonaManager.get_active_persona(user_id)
    
    # Retrieve based on generic keyword "history" to get recent or related context
    records = memory_system.search_memory(
        user_id=user_id,
        active_persona=active_persona_profile.name,
        query="conversation history context",
        limit=limit
    )
    
    return MemoryContextResponse(records=records)
