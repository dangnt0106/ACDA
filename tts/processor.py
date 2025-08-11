import os
import re
import datetime
import hashlib
import sys
os.environ["PATH"] += os.pathsep + os.path.abspath("ffmpeg/bin")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts.audio_utils import clean_filename, merge_audio_files, split_mixed_text, ensure_output_dir, split_vi_ja_sentences
from tts.google_tts_wrapper import GoogleTTS
from tts.edge_tts_wrapper import EdgeTTS
from config.config import OUTPUT_BASE_DIR
from utils.log import log
from typing import Tuple

edge_tts = EdgeTTS()

async def process_mixed_text_with_edge(input_text, ja_voice, vi_voice):
    if isinstance(ja_voice, list):
        ja_voice = ja_voice[0]
    if isinstance(vi_voice, list):
        vi_voice = vi_voice[0]
    try:
        # Sử dụng split_vi_ja_sentences để tách câu
        vi_sentences, ja_sentences = split_vi_ja_sentences(input_text)
        ja_text = " ".join(ja_sentences)
        vi_text = " ".join(vi_sentences)

        output_dir = ensure_output_dir(OUTPUT_BASE_DIR)
        output_paths = {}

        # Xử lý tiếng Nhật
        if ja_text:
            ja_path = os.path.join(output_dir, f"{ja_text}.mp3")
            try:
                await edge_tts.synthesize(ja_text, ja_voice, ja_path)
                log(f"[INFO] ✅ Japanese audio saved: {ja_path}")
                output_paths['ja'] = ja_path
            except Exception as e:
                log(f"[ERROR] ❌ Edge TTS Japanese error: {e}")
                ja_path = None

        # Xử lý tiếng Việt
        if vi_text:
            vi_hash = hashlib.md5(vi_text.encode('utf-8')).hexdigest()[:8]
            vi_path = os.path.join(output_dir, f"vn_{vi_hash}.mp3")
            try:
                await edge_tts.synthesize(vi_text, vi_voice, vi_path)
                log(f"[INFO] ✅ Vietnamese audio saved: {vi_path}")
                output_paths['vi'] = vi_path
            except Exception as e:
                log(f"[ERROR] ❌ Edge TTS Vietnamese error: {e}")
                vi_path = None

        if 'ja' in output_paths and 'vi' in output_paths:
            merged_path = os.path.join(output_dir, clean_filename(ja_text) + '_vn_merged.mp3')
            merged = merge_audio_files(output_paths['ja'], output_paths['vi'], merged_path)
            if merged:
                output_paths['merged'] = merged
                log(f'✅ Merged audio available at: {merged}')

        return output_paths
    except Exception as e:
        log(f'❌ Processing error: {e}')
        return None

google_tts = GoogleTTS()
def normalize(s):
    return re.sub(r'\s+', '', s).strip('。.!?？. ')

async def process_mixed_text_with_google(text: str, ja_voice: str, vi_voice: str) -> Tuple[str, str]:
    vi_sentences, ja_sentences = split_vi_ja_sentences(text)
    # Tạo list các câu theo đúng thứ tự xuất hiện
    # Tìm vị trí từng câu trong text gốc để giữ thứ tự
    

    all_sentences = []
    for s in re.split(r'[.。?!？]', text):
        s = s.strip()
        if not s:
            continue
        s_norm = normalize(s)
        found = False
        for ja in ja_sentences:
            if normalize(ja) == s_norm:
                all_sentences.append(('ja', s))
                found = True
                break
        if not found:
            for vi in vi_sentences:
                if normalize(vi) == s_norm:
                    all_sentences.append(('vi', s))
                    break

    output_dir = ensure_output_dir(OUTPUT_BASE_DIR)
    tts = GoogleTTS()
    audio_paths = []

    for lang, sentence in all_sentences:
        print(f"Đang synthesize: {lang} - {sentence}")
        if lang == 'ja':
            voice = ja_voice
            filename = f"ja_{hashlib.md5(sentence.encode('utf-8')).hexdigest()[:8]}.mp3"
        else:
            voice = vi_voice
            filename = f"vi_{hashlib.md5(sentence.encode('utf-8')).hexdigest()[:8]}.mp3"
        path = os.path.join(output_dir, filename)
        try:
            await tts.synthesize(sentence, voice, path)
            if os.path.exists(path):
                print(f"Đã tạo file: {path}")
                audio_paths.append(path)
            else:
                print(f"Không tạo được file: {path}")
        except Exception as e:
            print(f"[ERROR] ❌ Google TTS {lang} error: {e}")

    # Merge tất cả file audio theo đúng thứ tự
    if audio_paths:
        merged_path = os.path.join(output_dir, "merged_output.mp3")
        merge_audio_files(*audio_paths, output_path=merged_path)
        return "✅ Đã tạo file hợp nhất.", merged_path
    else:
        return "❌ Không tạo được file âm thanh.", ""

import asyncio

if __name__ == "__main__":
    # Ví dụ: tiếng Nhật và tiếng Việt
    text = "Tách văn bản tiếng Việt và tiếng Nhật. これは日本語のテキストです。"
    ja_voice = "ja-JP-NanamiNeural"
    vi_voice = "vi-VN-NamMinhNeural"
    ja_gg = "jp"
    vi_gg = "vi"
    result = asyncio.run(process_mixed_text_with_google(text, ja_gg, vi_gg))
    print(result)