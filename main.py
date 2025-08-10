import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend import get_together_ai_response

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    type: str  # 'text' or 'voice' — frontend can send this, backend doesn’t have to use it
    message: str

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    response_text = get_together_ai_response(chat_request.message)
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
