from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class UserAuth(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PersonaSelectRequest(BaseModel):
    persona_name: str  # Student, Business, Fitness, Personal

class ChatMessageRequest(BaseModel):
    message: str
    language: str = "English"  # "English" or "Malayalam"
    use_voice: bool = False

class ChatResponse(BaseModel):
    response: str
    persona: str
    emotion: str
    suggestions: List[str]
    voice_supported: bool
    memory_used: bool

class VoiceQueryRequest(BaseModel):
    audio_base64: str
    language: str = "English"

class AgentTaskRequest(BaseModel):
    task_type: str
    payload: Dict

class MemoryRecord(BaseModel):
    user_id: str
    persona: str
    content: str
    timestamp: str

class MemoryContextResponse(BaseModel):
    records: List[MemoryRecord]

class PersonaProfile(BaseModel):
    name: str
    tone: str
    reasoning_depth: str
    allowed_domains: List[str]
    system_prompt: str
