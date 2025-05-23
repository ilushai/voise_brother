from cfg import OPENAI_API_KEY
import requests
import logging

def audio_to_text(audio_path, language="ru"):
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    files = {
        "file": open(audio_path, "rb"),
        "model": (None, "whisper-1"),
        "language": (None, language)
    }
    response = requests.post(url, headers=headers, files=files)
    try:
        response.raise_for_status()
        data = response.json()
        logging.info(f"[Whisper] Ответ: {data}")
        return data["text"]
    except Exception as e:
        logging.error(f"[Whisper] Ошибка: {response.text}")
        raise e
