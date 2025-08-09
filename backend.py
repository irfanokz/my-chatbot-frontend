# file: backend.py

from fastapi import FastAPI
from pydantic import BaseModel
from utils import speak_with_elevenlabs  # your existing utils.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

def get_together_ai_response(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error from Together AI: {response.text}"

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    bot_response = get_together_ai_response(user_message)
    # We won't do TTS here to keep it simple
    return {"reply": bot_response}
