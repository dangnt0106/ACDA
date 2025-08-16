import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pydub import AudioSegment
from utils.log import log
import re
import datetime
import numpy as np

# ==== TEXT PROCESSING ====
def split_mixed_text(text: str) -> tuple[str, str]:
    import re
    parts = [p.strip() for p in re.split(r'[。.／/→?]', text, maxsplit=1)]
    return parts if len(parts) == 2 else (parts[0], "")

# ==== AUDIO UTILITIES ====
from utils.file_utils import clean_filename

# ==== AUDIO UTILITIES ====
from utils.file_utils import ensure_output_dir

# ==== AUDIO MERGING ====
from utils.audio_utils import merge_audio_files
    
def load_audio_to_np(file_path: str) -> tuple[int, np.ndarray]:
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return audio.frame_rate, samples

def merge_audios_to_np(audios: list[tuple[int, np.ndarray]]) -> tuple[int, np.ndarray]:
    if not audios:
        return 0, np.array([])

    sample_rate = audios[0][0]
    merged = np.concatenate([a[1] for a in audios if a[1] is not None])
    return sample_rate, merged

from utils.text_utils import split_vi_ja_sentences

# Ví dụ sử dụng:
# vi, ja = split_vi_ja_sentences("それよりこれの方がいいですよ。Cái đó tốt hơn cái này。確かに.Đúng。ベビーベッドは買うよりレンタルの方がいいですよ。Tốt hơn hết là bạn nên thuê một chiếc giường trẻ em thay vì mua nó。確かに.Chắc chắn.")
# print("Tiếng Việt:", vi)
# print("Tiếng Nhật:", ja)