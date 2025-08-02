from gtts import gTTS
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts.base import BaseTTS

class GoogleTTS(BaseTTS):
    async def synthesize(self, text: str, voice: str, output_path: str) -> str:
        # Xác định ngôn ngữ từ voice name
        lang = 'vi' if 'vi' in voice.lower() else 'ja'

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Sinh audio
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"[ERROR] Google TTS failed: {e}")
            return ""
