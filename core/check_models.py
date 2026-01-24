import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Scanning available models...")
try:
    # This simply grabs the list and prints the name. No filtering.
    for m in client.models.list():
        print(f"📦 FOUND: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")
