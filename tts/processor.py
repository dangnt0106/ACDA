import os
import re
import datetime
import hashlib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts.audio_utils import clean_filename, merge_audio_files,split_mixed_text, ensure_output_dir
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
        content = input_text.strip()
        parts = [p.strip() for p in re.split(r'[。／.→]', content, maxsplit=1)]

        ja_text, vi_text = "", ""
        if len(parts) == 1:
            ja_text = parts[0] if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[0]) else ""
            vi_text = parts[0] if not ja_text else ""
        elif len(parts) == 2:
            if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[0]):
                ja_text = parts[0]
                vi_text = parts[1]
            else:
                vi_text = parts[0]
                ja_text = parts[1]

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

async def process_mixed_text_with_google(text: str, ja_voice: str, vi_voice: str) -> Tuple[str, str]:
    ja_text, vi_text = split_mixed_text(text)

    output_dir = ensure_output_dir(OUTPUT_BASE_DIR)
        
    content = text.strip()
    parts = [p.strip() for p in re.split(r'[。／.→]', content, maxsplit=1)]

    ja_text, vi_text = "", ""
    if len(parts) == 1:
        ja_text = parts[0] if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[0]) else ""
        vi_text = parts[0] if not ja_text else ""
    elif len(parts) == 2:
        if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[0]):
            ja_text = parts[0]
            vi_text = parts[1]
        elif re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[1]):
            vi_text = parts[0]
            ja_text = parts[1]
        else:
            vi_text = parts[0]
    ja_path = None
    vi_path = None
    tts = GoogleTTS()

    # Xử lý tiếng Nhật
    if ja_text:
        ja_path = os.path.join(output_dir, f"{ja_text}.mp3")
        try:
            await tts.synthesize(ja_text, ja_voice, ja_path)
            print(f"[INFO] ✅ Japanese audio saved: {ja_path}")
        except Exception as e:
            print(f"[ERROR] ❌ Google TTS Japanese error: {e}")
            ja_path = None

    # Xử lý tiếng Việt
    if vi_text:
        vi_hash = hashlib.md5(vi_text.encode('utf-8')).hexdigest()[:8]
        vi_path = os.path.join(output_dir, f"vn_{vi_hash}.mp3")
        try:
            await tts.synthesize(vi_text, vi_voice, vi_path)
            print(f"[INFO] ✅ Vietnamese audio saved: {vi_path}")
        except Exception as e:
            print(f"[ERROR] ❌ Google TTS Vietnamese error: {e}")
            vi_path = None

    # Ghép file nếu có đủ
    if ja_path and vi_path:
        merged_path = os.path.join(output_dir, f"{ja_text}_merged.mp3")
        merge_audio_files(ja_path, vi_path, merged_path)
        return "✅ Đã tạo file hợp nhất.", merged_path
    elif ja_path:
        return "✅ Đã tạo file tiếng Nhật.", ja_path
    elif vi_path:
        return "✅ Đã tạo file tiếng Việt.", vi_path
    else:
        return "❌ Không tạo được file âm thanh.", ""

# import asyncio
# from tts.processor import process_mixed_text_with_edge

# if __name__ == "__main__":
#     # Ví dụ: tiếng Nhật và tiếng Việt
#     text = "私は猫が好きです. Tôi thích mèo"
#     ja_voice = "ja-JP-NanamiNeural"
#     vi_voice = "vi-VN-NamMinhNeural"

#     result = asyncio.run(process_mixed_text_with_edge(text, ja_voice, vi_voice))
#     print(result)