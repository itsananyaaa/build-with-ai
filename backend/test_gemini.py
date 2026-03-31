from dotenv import load_dotenv
load_dotenv() # Force load to be safe

from app.services.response_engine import response_engine
from app.services.persona_manager import PersonaManager
from app.core.config import settings
import sys
import json

def test():
    if not settings.GEMINI_API_KEY:
        print("FAIL: GEMINI_API_KEY is not set or not loaded!")
        sys.exit(1)
    print(f"PASS: GEMINI_API_KEY loaded (ends in {settings.GEMINI_API_KEY[-4:]})")

    try:
        persona = PersonaManager.get_persona("Student")
        print("\nTesting LLM Generation with 'Student' Persona...")
        
        result = response_engine.generate_response(
            user_msg="Can you explain how photosynthesis works in 2 sentences?",
            persona=persona,
            memory_context="",
            language="English"
        )
        print("\n----- SUCCESS: RESPONSE -----")
        print(json.dumps(result, indent=2))
        print("------------------------------")
    except Exception as e:
        print(f"\nFAIL: Failed to generate response: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test()
