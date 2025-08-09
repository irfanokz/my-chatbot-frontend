import os
from dotenv import load_dotenv
import requests
from utils import speak_with_elevenlabs  # Your existing TTS function
import speech_recognition as sr

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_together_ai_response(prompt):
    try:
        url = "https://api.together.xyz/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error from Together AI: {response.text}"

    except Exception as e:
        return f"Error communicating with Together AI: {e}"

def listen_to_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak now.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

if __name__ == "__main__":
    print("AI Chatbot with Voice and Text (type 'exit' to quit)")
    while True:
        choice = input("Type 'voice' to speak or 'text' to type your message: ").lower()
        if choice == "exit":
            break

        if choice == 'voice':
            user_input = listen_to_mic()
            if not user_input:
                continue  # Retry if nothing understood
        elif choice == 'text':
            user_input = input("You: ")
        else:
            print("Invalid choice. Please type 's' or 't'.")
            continue

        if user_input.lower() == "exit":
            break

        ai_response = get_together_ai_response(user_input)
        print("Bot:", ai_response)
        speak_with_elevenlabs(ai_response)
