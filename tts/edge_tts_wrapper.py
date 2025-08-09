# tts/edge_tts_wrapper.py
import edge_tts
import os
from tts.audio_utils import ensure_output_dir
from utils.log import log
from tts.base import BaseTTS


class EdgeTTS(BaseTTS):
    async def synthesize(self, text: str, voice: str, output_path: str) -> str:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return output_path
    

async def convert_text_to_speech(text: str, voice: str, output_path: str):
    try:       
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(output_path)
        return output_path
    except Exception as e:
        log(f"❌ TTS generation failed: {e}")
        return None
