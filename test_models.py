import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API Key")
    exit()

client = genai.Client(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
    "gemini-2.0-flash-exp",
    "gemini-exp-1206"
]

print("Testing models...")
for model_name in models_to_test:
    try:
        print(f"Testing {model_name}...", end=" ")
        client.models.generate_content(model=model_name, contents="Hi")
        print("SUCCESS!")
        print(f"WORKING MODEL: {model_name}")
        break
    except Exception as e:
        print(f"Failed: {e}")
