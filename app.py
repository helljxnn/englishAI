import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
    
    system_instruction = """
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
else:
    print("WARNING: GEMINI_API_KEY not found in .env file.")
    client = None

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    if not client:
        return jsonify({"error": "API Key not configured. Please check your .env file."}), 500

    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Para modelos Gemma, incluimos las instrucciones del sistema en el mensaje
        full_message = f"{system_instruction}\n\nUser: {user_message}\n\nAssistant:"
        
        response = client.models.generate_content(
            model="gemma-3-4b-it",
            config=types.GenerateContentConfig(
                temperature=0.7,
            ),
            contents=full_message
        )
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"Error with gemma-3-4b-it: {e}")
        return jsonify({"error": f"Model failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
