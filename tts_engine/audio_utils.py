import os
from pydub import AudioSegment
import utils.log as log
import re
# ==== AUDIO UTILITIES ====
def clean_filename(text: str) -> str:
    text = re.sub(r'[<>:"/\\|?*\n\r\t]', '', text)  
    text = text.strip().replace(" ", "_").replace(".", "")
    #text = text.strip()
    return text

# ==== AUDIO UTILITIES ====
def ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)

# ==== AUDIO MERGING ====
def merge_audio_files(file1: str, file2: str, output_path: str) -> str:
    try:
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise FileNotFoundError("Input audio files not found.")

        sound1 = AudioSegment.from_file(file1)
        sound2 = AudioSegment.from_file(file2)

        combined = sound1 + sound2
        combined.export(output_path, format="mp3")
        #log(f"Merged audio saved: {output_path}")
        return output_path
    except Exception as e:
        log(f"Merging error: {e}")
        return None