import os
from dotenv import load_dotenv
import openai

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No API key found in .env file!")
    exit(1)

try:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, are you working?"}],
        max_tokens=50,
    )
    print("OpenAI API call succeeded!\nResponse:")
    print(response.choices[0].message.content)
except Exception as e:
    print("OpenAI API call failed:")
    print(e) 