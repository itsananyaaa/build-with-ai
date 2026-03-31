from fastapi import APIRouter, Depends
from app.models.schemas import ChatMessageRequest, ChatResponse
from app.services.persona_manager import PersonaManager
from app.services.memory_system import memory_system
from app.services.response_engine import response_engine
from app.core.security import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatMessageRequest, current_user: dict = Depends(get_current_user)):
    """
    Receives user message, checks memory of active persona, and responds via Gemini API
    Returns frontend-friendly structured JSON
    """
    user_id = current_user["user_id"]
    active_persona_profile = PersonaManager.get_active_persona(user_id)
    
    # Vector Search Context Retrieval (Isolates by persona/domain implicitly)
    relevant_memories = memory_system.search_memory(
        user_id=user_id,
        active_persona=active_persona_profile.name,
        query=request.message,
        limit=3
    )
    
    memory_context = "\n".join([m.content for m in relevant_memories])
    
    # Generate context-aware, emotion-aware response
    ai_result = response_engine.generate_response(
        user_msg=request.message,
        persona=active_persona_profile,
        memory_context=memory_context,
        language=request.language
    )
    
    # Save interaction back to Persona's local Vector Memory
    try:
        memory_system.add_memory(
            user_id=user_id,
            persona=active_persona_profile.name,
            content=f"User ({request.language}): {request.message} | AI: {ai_result['response']}"
        )
    except Exception as e:
        logger.error(f"Failed to record memory: {e}")

    # Enforce frontend compatibility strict format
    response_model = ChatResponse(
        response=ai_result.get("response", ""),
        persona=ai_result.get("persona", active_persona_profile.name),
        emotion=ai_result.get("emotion", "neutral"),
        suggestions=ai_result.get("suggestions", []),
        voice_supported=True,
        memory_used=ai_result.get("memory_used", False)
    )

    return response_model
