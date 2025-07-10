import os
from dotenv import load_dotenv
import openai

print("Script started")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print("API Key loaded:", bool(api_key))

if not api_key:
    print("No API key found in .env file!")
    exit(1)

try:
    client = openai.OpenAI(api_key=api_key)
    print("Client created")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=10,
    )
    print("RESPONSE:", response.choices[0].message.content)
except Exception as e:
    print("ERROR:", e)