class EmotionDetector:
    @staticmethod
    def detect_emotion(text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ['stress', 'hard', 'tired', 'overwhelmed', 'stuck']):
            return 'stressed'
        elif any(word in text_lower for word in ['lets go', 'ready', 'pumped', 'excited', 'motivated']):
            return 'motivated'
        elif any(word in text_lower for word in ['what', 'confused', 'dont understand', 'how to', 'explain']):
            return 'confused'
        return 'neutral'

    @staticmethod
    def detect_intent(text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ['study', 'learn', 'course', 'exam']):
            return 'study'
        elif any(word in text_lower for word in ['business', 'report', 'meeting', 'strategy', 'roi']):
            return 'business'
        elif any(word in text_lower for word in ['workout', 'gym', 'run', 'diet', 'fitness']):
            return 'fitness'
        return 'general'

    @staticmethod
    def analyze(text: str) -> dict:
        return {
            "emotion": EmotionDetector.detect_emotion(text),
            "intent": EmotionDetector.detect_intent(text)
        }
