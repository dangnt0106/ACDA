import os
import re
import datetime
import hashlib
from tts_engine.audio_utils import clean_filename, merge_audio_files
from tts_engine.edge_tts_wrapper import convert_text_to_speech
from config.config import OUTPUT_BASE_DIR
from utils.log import log

async def process_mixed_text(input_text, ja_voice, vi_voice):
    if isinstance(ja_voice, list):
        ja_voice = ja_voice[0]
    if isinstance(vi_voice, list):
        vi_voice = vi_voice[0]
    
    try:
        content = input_text.strip()
        parts = [p.strip() for p in re.split(r'[。／.]', content, maxsplit=1)]

        ja_text, vi_text = "", ""
        if len(parts) == 1:
            ja_text = parts[0] if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', parts[0]) else ""
            vi_text = parts[0] if not ja_text else ""
        elif len(parts) == 2:
            ja_text, vi_text = parts

        output_dir = os.path.join(OUTPUT_BASE_DIR, datetime.datetime.now().strftime('%m%d'))
        os.makedirs(output_dir, exist_ok=True)

        output_paths = {}

        if ja_text:
            ja_path = await convert_text_to_speech(ja_text, ja_voice, output_dir)
            if ja_path:
                output_paths['ja'] = ja_path
                log(f'✅ Japanese audio saved: {ja_path}')
        if vi_text:
            vi_hash = hashlib.md5(vi_text.encode()).hexdigest()[:6]
            vi_filename = f'vn_{vi_hash}.mp3'
            vi_path = await convert_text_to_speech(vi_text, vi_voice, output_dir)
            if vi_path:
                output_paths['vi'] = vi_path
                log(f'✅ Vietnamese audio saved: {vi_path}')

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
