import requests
import os
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "FGY2WhTYpPnrIDTdsKH5"

# Path to your temp_audio folder inside the project directory
TEMP_AUDIO_DIR = os.path.join(os.getcwd(), "temp_audio")

def speak_with_elevenlabs(text):
    try:
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
            # Save audio to a file in temp_audio folder
            temp_filename = os.path.join(TEMP_AUDIO_DIR, "temp_audio.mp3")
            with open(temp_filename, "wb") as f:
                f.write(response.content)

            # Play the audio
            playsound(temp_filename)

            # Remove the file after playing
            os.remove(temp_filename)
        else:
            print(f"Error from ElevenLabs: {response.text}")

    except Exception as e:
        print(f"Error communicating with ElevenLabs: {e}")
