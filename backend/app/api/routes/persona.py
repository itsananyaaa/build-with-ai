from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.schemas import PersonaSelectRequest, PersonaProfile
from app.services.persona_manager import PersonaManager
from app.core.security import get_current_user

router = APIRouter(prefix="/persona", tags=["persona"])

@router.get("/list", response_model=List[PersonaProfile])
async def list_personas(current_user: dict = Depends(get_current_user)):
    """
    Returns list of available personas
    """
    return PersonaManager.list_personas()

@router.post("/select")
async def select_persona(request: PersonaSelectRequest, current_user: dict = Depends(get_current_user)):
    """
    Selects the active persona constraint for memory context separation and response tone
    """
    success = PersonaManager.set_active_persona(current_user["user_id"], request.persona_name)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid persona name provided.")
    return {"status": "success", "active_persona": request.persona_name.capitalize()}
