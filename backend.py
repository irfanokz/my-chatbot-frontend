import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_together_ai_response(prompt: str) -> str:
    try:
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant that explains things step-by-step, "
                        "like ChatGPT-5. Break your answers into short sections, use clear formatting, "
                        "bullet points, and examples where useful."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error from Together AI: {response.text}"

    except Exception as e:
        return f"Error communicating with Together AI: {e}"
