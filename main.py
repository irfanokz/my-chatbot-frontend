from fastapi.responses import StreamingResponse
from together import Together

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    def generate():
        stream = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct",
            messages=[{"role": "user", "content": chat_request.message}],
            stream=True
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.get("content", "")
            if delta:
                yield delta
    return StreamingResponse(generate(), media_type="text/plain")
