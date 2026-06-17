import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDztfeyNxLS2Z6RxKmTqio2-B3jbAKnCEg")
genai.configure(api_key=api_key)

print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")
