import requests
import os
from playsound import playsound
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "FGY2WhTYpPnrIDTdsKH5"

# Create temp_audio directory if it doesn't exist
TEMP_AUDIO_DIR = os.path.join(os.getcwd(), "temp_audio")
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

def speak_with_elevenlabs(text: str):
    """
    Sends text to ElevenLabs API, saves the generated speech in temp_audio folder,
    plays it, and deletes the file afterwards.
    """
    try:
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY is missing. Please set it in Railway environment variables.")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            temp_filename = os.path.join(TEMP_AUDIO_DIR, "temp_audio.mp3")

            with open(temp_filename, "wb") as f:
                f.write(response.content)

            try:
                playsound(temp_filename)
            except Exception as e:
                print(f"Audio playback failed: {e}")

            os.remove(temp_filename)
        else:
            print(f"Error from ElevenLabs: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error communicating with ElevenLabs: {e}")
