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
def clean_filename(text: str) -> str:
    text = re.sub(r'[<>:"\\|?*\n\r\t]', '', text)
    return text

# ==== AUDIO UTILITIES ====
def ensure_output_dir(path: str):
    today = datetime.datetime.now().strftime("%m%d")
    out_dir = os.path.join(path, today)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir

# ==== AUDIO MERGING ====
def merge_audio_files(*audio_paths, output_path):
    from pydub import AudioSegment
    merged = None
    for path in audio_paths:
        audio = AudioSegment.from_file(path)
        if merged is None:
            merged = audio
        else:
            merged += audio
    if merged:
        merged.export(output_path, format="mp3")
        return output_path
    return None
    
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

def split_vi_ja_sentences(text: str) -> tuple[list[str], list[str]]:
    text = re.sub(r'\b[A-Z]:\s*', '', text)
    ja_pattern = r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]'
    vi_pattern = r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]'
    # Tách câu theo dấu câu và cả dấu xuống dòng, giữ lại dấu câu cuối nếu có
    sentences = re.split(r'([.。?!？\n\r])', text)
    merged_sentences = []
    buf = ''
    for part in sentences:
        if part in ['.', '。', '?', '！', '!', '？', '\n', '\r']:
            buf += part
            merged_sentences.append(buf.strip())
            buf = ''
        else:
            buf += part
    if buf.strip():
        merged_sentences.append(buf.strip())
    vi_sentences = []
    ja_sentences = []
    for s in merged_sentences:
        s = s.strip()
        if not s:
            continue
        # Nếu có ký tự tiếng Nhật thì là câu Nhật
        if re.search(ja_pattern, s):
            ja_sentences.append(s)
        # Nếu có ký tự tiếng Việt thì là câu Việt
        elif re.search(vi_pattern, s):
            vi_sentences.append(s)
    return vi_sentences, ja_sentences

# Ví dụ sử dụng:
# vi, ja = split_vi_ja_sentences("それよりこれの方がいいですよ。Cái đó tốt hơn cái này。確かに.Đúng。ベビーベッドは買うよりレンタルの方がいいですよ。Tốt hơn hết là bạn nên thuê một chiếc giường trẻ em thay vì mua nó。確かに.Chắc chắn.")
# print("Tiếng Việt:", vi)
# print("Tiếng Nhật:", ja)