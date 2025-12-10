import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"Key starts with: {api_key[:5]}...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello")
        print("API Call Successful")
    except Exception as e:
        print(f"API Call Failed: {e}")
