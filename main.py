import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend import get_together_ai_response

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    type: str  # frontend can send 'text' or 'voice' — backend ignores this for now
    message: str

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    # Only process the text message
    response_text = get_together_ai_response(chat_request.message)
    return {"response": response_text}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Changed default to 8080 for Railway
    uvicorn.run(app, host="0.0.0.0", port=port)
