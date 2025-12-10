import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        self.system_instruction = """
        You are an English language teacher AI. Your sole purpose is to help users learn, practice, and improve their English skills.
        
        RULES:
        1.  **Strict Context**: You must ONLY answer questions related to:
            - English grammar, vocabulary, spelling, and punctuation.
            - Pronunciation and phonetics.
            - Reading comprehension and writing skills.
            - Cultural aspects of English-speaking countries (UK, USA, Australia, etc.) as they relate to language learning.
            - Translation to/from English for learning purposes.
        
        2.  **Out of Bounds**: If a user asks about ANY other topic (e.g., math, coding, politics, history unrelated to language, personal advice, entertainment news), you must politely REFUSE to answer.
            - Example refusal: "I am sorry, but I can only help you with learning English. Let's get back to our lesson!"
            - Do not provide the requested information even if you know it.
        
        3.  **Persona**: Be encouraging, patient, and polite. Use clear and simple English suitable for learners, adjusting complexity based on the user's input.
        
        4.  **Correction**: If the user makes a mistake, gently correct them and explain the rule.
        """
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
    
    def is_configured(self):
        return self.client is not None
    
    def generate_response(self, user_message):
        if not self.client:
            raise Exception("API Key not configured")
        
        # Para modelos Gemma, incluimos las instrucciones del sistema en el mensaje
        full_message = f"{self.system_instruction}\n\nUser: {user_message}\n\nAssistant:"
        
        response = self.client.models.generate_content(
            model="gemma-3-4b-it",
            config=types.GenerateContentConfig(
                temperature=0.7,
            ),
            contents=full_message
        )
        
        return response.text