import os
from dotenv import load_dotenv
import requests

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

response = requests.get(
    f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
)

modelos = response.json().get("models", [])

print("Modelos con generateContent disponible:")
for m in modelos:
    if "generateContent" in m.get("supportedGenerationMethods", []):
        print(f"  - {m['name']}")