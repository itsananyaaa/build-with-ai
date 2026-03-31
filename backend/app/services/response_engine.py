import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import ChatResponse, PersonaProfile
from app.services.emotion_detector import EmotionDetector
import json
import logging

logger = logging.getLogger(__name__)

# Only configure if API key is provided
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class AIResponseEngine:
    def __init__(self):
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.active = True if settings.GEMINI_API_KEY else False
        except Exception as e:
            logger.error(f"Cannot initialize Gemini: {e}")
            self.active = False

    def generate_response(self, user_msg: str, persona: PersonaProfile, memory_context: str, language: str) -> dict:
        analysis = EmotionDetector.analyze(user_msg)
        emotion = analysis["emotion"]

        prompt = f"""
        You are PersonaAI, an advanced multi-persona intelligent assistant.
        Your core capability is to dynamically adapt your personality, tone, and response style based on the selected persona.
        
        Core Instructions:
        - Always use the provided active persona: {persona.name}.
        - Adapt your tone, vocabulary, and response structure accordingly.
        - Keep responses relevant, clear, and useful.
        - Do NOT mention that you are switching personas.
        - Maintain consistency within your response.
        - Use clear formatting (bullets, headings) when needed.
        - Keep answers concise but insightful.

        Active Persona System: {persona.system_prompt}
        Required Tone: {persona.tone}
        Reasoning Depth: {persona.reasoning_depth}
        User Emotion/State: {emotion}
        Language: Respond primarily in {language}.
        
        Memory Context (Available Knowledge for this persona):
        {memory_context}
        
        Given the above role and constraints, respond to the user.
        User Message: "{user_msg}"

        Output MUST be valid JSON format only, exactly matching this structure (no markdown tags):
        {{
            "response": "your generated response text here",
            "suggestions": ["suggestion 1", "suggestion 2"]
        }}
        """

        if not self.active:
            # Mock response for testing without API key
            return {
                "response": f"[(Mock Mode) {persona.name} ({emotion}) - {language}] Here is a placeholder response.",
                "persona": persona.name,
                "emotion": emotion,
                "suggestions": ["Try again later", "Provide an API key"],
                "voice_supported": True,
                "memory_used": len(memory_context) > 0
            }

        try:
            result = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            data = json.loads(result.text)
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            data = {
                "response": "I apologize, but I could not formulate a response at the moment.",
                "suggestions": []
            }

        return {
            "response": data.get("response", ""),
            "persona": persona.name,
            "emotion": emotion,
            "suggestions": data.get("suggestions", []),
            "voice_supported": True,
            "memory_used": len(memory_context) > 0
        }

response_engine = AIResponseEngine()
