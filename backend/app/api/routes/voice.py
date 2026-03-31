from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import VoiceQueryRequest, ChatResponse, ChatMessageRequest
from app.services.voice_pipeline import voice_pipeline
from app.api.routes.chat import chat_message
from app.core.security import get_current_user

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/query", response_model=ChatResponse)
async def voice_query(request: VoiceQueryRequest, current_user: dict = Depends(get_current_user)):
    """
    Handles speech-to-text input, processes via conversational engine, 
    and handles English / Malayalam
    """
    
    # Process speech-to-text input (Mock implementation returning simulated text)
    processed_text = voice_pipeline.process_audio(request.audio_base64, request.language)
    
    if not processed_text:
        raise HTTPException(status_code=400, detail="Voice processing failed or audio missing.")
    
    # Run the standard context-aware flow
    chat_req = ChatMessageRequest(
        message=processed_text,
        language=request.language,
        use_voice=True
    )
    
    # Let normal chat response handle memory and AI retrieval
    chat_response = await chat_message(chat_req, current_user)
    
    # The AI returns voice_supported: True
    # Implementation could optionally return an audio base64 payload to the frontend,
    # but conforming strictly to the frontend desired JSON as per requirements here.
    return chat_response
