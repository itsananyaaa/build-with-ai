from typing import Dict, List
from app.models.schemas import PersonaProfile
import redis
import json
from app.core.config import settings

# A bit of state for active personas per user
# In production, use Redis. We'll use a simple in-memory dict for local testing, 
# but Redis is already in requirements.
import os

PERSONA_STORE: Dict[str, PersonaProfile] = {
    "Mentor": PersonaProfile(
        name="Mentor",
        tone="clear, structured, educational, encouraging",
        reasoning_depth="step-by-step educational explanations",
        allowed_domains=["mentor_memory"],
        system_prompt="Your active persona is 'Mentor'. Provide clear, structured, educational explanations. Encourage learning."
    ),
    "Friend": PersonaProfile(
        name="Friend",
        tone="casual, supportive, empathetic, conversational",
        reasoning_depth="thoughtful, emotional, conversational",
        allowed_domains=["friend_memory"],
        system_prompt="Your active persona is 'Friend'. Be casual, supportive, empathetic, and conversational."
    ),
    "Analyst": PersonaProfile(
        name="Analyst",
        tone="logical, data-driven, concise, objective",
        reasoning_depth="analytical, highly structured insights",
        allowed_domains=["analyst_memory"],
        system_prompt="Your active persona is 'Analyst'. Be logical, data-driven, concise, and objective."
    ),
    "Creative": PersonaProfile(
        name="Creative",
        tone="imaginative, expressive, idea-generating",
        reasoning_depth="brainstorming, expressive",
        allowed_domains=["creative_memory"],
        system_prompt="Your active persona is 'Creative'. Be imaginative, expressive, and generate ideas."
    ),
    "Professional": PersonaProfile(
        name="Professional",
        tone="formal, precise, business-oriented",
        reasoning_depth="formal, strategic",
        allowed_domains=["professional_memory"],
        system_prompt="Your active persona is 'Professional'. Be formal, precise, and business-oriented."
    )
}

# In-memory store fallback if Redis is not running
USER_ACTIVE_PERSONA: Dict[str, str] = {}

class PersonaManager:
    @staticmethod
    def get_persona(name: str) -> PersonaProfile:
        persona = PERSONA_STORE.get(name.capitalize())
        if not persona:
            return PERSONA_STORE["Professional"] # Fallback
        return persona

    @staticmethod
    def list_personas() -> List[PersonaProfile]:
        return list(PERSONA_STORE.values())

    @staticmethod
    def set_active_persona(user_id: str, persona_name: str) -> bool:
        if persona_name.capitalize() not in PERSONA_STORE:
            return False
        USER_ACTIVE_PERSONA[user_id] = persona_name.capitalize()
        # Redis integration placeholder
        return True

    @staticmethod
    def get_active_persona(user_id: str) -> PersonaProfile:
        active_name = USER_ACTIVE_PERSONA.get(user_id, "Professional")
        return PERSONA_STORE[active_name]
