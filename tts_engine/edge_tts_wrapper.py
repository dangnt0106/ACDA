# tts/edge_tts_wrapper.py
import edge_tts
import os
from tts_engine.audio_utils import ensure_directory
from utils.log import log

async def convert_text_to_speech(text: str, voice: str, output_dir: str):
    try:
        ensure_directory(output_dir)
        filename = f"{text}.mp3"
        output_path = os.path.join(output_dir, filename)

        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(output_path)

        log(f"Audio saved: {output_path}")
        return output_path
    except Exception as e:
        log(f"❌ TTS generation failed: {e}")
        return None
