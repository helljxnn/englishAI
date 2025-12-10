import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
    try:
        print("Listing available models:")
        # The new SDK might have a different way to list models, or we can try a simple generation to test specific names.
        # But let's try to list if possible. The SDK documentation suggests client.models.list()
        for m in client.models.list():
            print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")
else:
    print("No API Key found")
