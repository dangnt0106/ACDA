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
    def normalize(s):
        return re.sub(r'\s+', '', s).strip('。.!?？. ')
    if isinstance(ja_voice, list):
        ja_voice = ja_voice[0]
    if isinstance(vi_voice, list):
        vi_voice = vi_voice[0]
    try:
        # Log sentences split by split_vi_ja_sentences for debugging
        vi_sentences, ja_sentences = split_vi_ja_sentences(input_text)
        # Synthesize trực tiếp từ danh sách đã tách, giữ thứ tự xuất hiện
        all_sentences = []
        # Tách text thành từng câu, xác định ngôn ngữ, giữ thứ tự
        sentences = re.split(r'([.。?!？\n\r])', input_text)
        buf = ''
        for part in sentences:
            if part in ['.', '。', '?', '！', '!', '？', '\n', '\r']:
                buf += part
                s = buf.strip()
                if not s:
                    buf = ''
                    continue
                if any(re.search(pattern, s) for pattern in [r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]']):
                    all_sentences.append(('ja', s))
                elif any(re.search(pattern, s) for pattern in [r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]']):
                    all_sentences.append(('vi', s))
                buf = ''
            else:
                buf += part
        if buf.strip():
            s = buf.strip()
            if any(re.search(pattern, s) for pattern in [r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]']):
                all_sentences.append(('ja', s))
            elif any(re.search(pattern, s) for pattern in [r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]']):
                all_sentences.append(('vi', s))

        output_dir = ensure_output_dir(OUTPUT_BASE_DIR)
        audio_paths = []
        jp_count = 1
        vi_count = 1

        for lang, sentence in all_sentences:
            # ...existing code...
            if lang == 'ja':
                voice = ja_voice
                filename = f"jp_{jp_count}.mp3"
                jp_count += 1
            else:
                voice = vi_voice
                filename = f"vi_{vi_count}.mp3"
                vi_count += 1
            path = os.path.join(output_dir, filename)
            try:
                await edge_tts.synthesize(sentence, voice, path)
                if os.path.exists(path):
                    audio_paths.append(path)
            except Exception as e:
                pass

        # Merge tất cả file audio theo đúng thứ tự
        output_paths = {}
        if audio_paths:
            merged_path = os.path.join(output_dir, "merged_output.mp3")
            merge_audio_files(*audio_paths, output_path=merged_path)
            output_paths['merged'] = merged_path
            log(f'✅ Merged audio available at: {merged_path}')
        return output_paths
    except Exception as e:
        log(f'❌ Processing error: {e}')
        return None

google_tts = GoogleTTS()
def normalize(s):
    return re.sub(r'\s+', '', s).strip('。.!?？. ')

async def process_mixed_text_with_google(text: str, ja_voice: str, vi_voice: str) -> Tuple[str, str]:
    vi_sentences, ja_sentences = split_vi_ja_sentences(text)
    # Synthesize trực tiếp từ danh sách đã tách, giữ thứ tự xuất hiện
    all_sentences = []
    sentences = re.split(r'([.。?!？\n\r])', text)
    buf = ''
    for part in sentences:
        if part in ['.', '。', '?', '！', '!', '？', '\n', '\r']:
            buf += part
            s = buf.strip()
            if not s:
                buf = ''
                continue
            if any(re.search(pattern, s) for pattern in [r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]']):
                all_sentences.append(('ja', s))
            elif any(re.search(pattern, s) for pattern in [r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]']):
                all_sentences.append(('vi', s))
            buf = ''
        else:
            buf += part
    if buf.strip():
        s = buf.strip()
        if any(re.search(pattern, s) for pattern in [r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]']):
            all_sentences.append(('ja', s))
        elif any(re.search(pattern, s) for pattern in [r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]']):
            all_sentences.append(('vi', s))

    output_dir = ensure_output_dir(OUTPUT_BASE_DIR)
    tts = GoogleTTS()
    audio_paths = []
    jp_count = 1
    vi_count = 1

    for lang, sentence in all_sentences:
    # ...existing code...
        if lang == 'ja':
            voice = ja_voice
            filename = f"jp_{jp_count}.mp3"
            jp_count += 1
        else:
            voice = vi_voice
            filename = f"vi_{vi_count}.mp3"
            vi_count += 1
        path = os.path.join(output_dir, filename)
        try:
            await tts.synthesize(sentence, voice, path)
            if os.path.exists(path):
                audio_paths.append(path)
        except Exception as e:
            pass

    # Merge tất cả file audio theo đúng thứ tự
    if audio_paths:
        merged_path = os.path.join(output_dir, "merged_output.mp3")
        merge_audio_files(*audio_paths, output_path=merged_path)
        return "✅ Đã tạo file hợp nhất.", merged_path
    else:
        return "❌ Không tạo được file âm thanh.", ""

# import asyncio

# if __name__ == "__main__":
#     # Ví dụ: tiếng Nhật và tiếng Việt
#     text = "Tôi thích mèo。私は猫が好きです。Tôi thích gà。私は好きです?Tôi thích chó.\n" \
#            "A:少しも分からない。\n" \
#            "B:Một chút cũng không biết."
#     ja_voice = "ja-JP-NanamiNeural"
#     vi_voice = "vi-VN-NamMinhNeural"
#     ja_gg = "jp"
#     vi_gg = "vi"
#     #result = asyncio.run(process_mixed_text_with_google(text, ja_gg, vi_gg))
#     result = asyncio.run(process_mixed_text_with_edge(text, ja_voice, vi_voice))
#     print(result)