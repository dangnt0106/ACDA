import os
import re
from utils.audio_utils import merge_audio_files
from utils.text_utils import split_vi_ja_sentences
from utils.file_utils import ensure_output_dir
from tts.google_tts_wrapper import GoogleTTS
from tts.edge_tts_wrapper import EdgeTTS
from config.config import OUTPUT_BASE_DIR
from utils.log import log


edge_tts = EdgeTTS()

async def process_mixed_text_with_edge(input_text, ja_voice, vi_voice):
    if isinstance(ja_voice, list):
        ja_voice = ja_voice[0]
    if isinstance(vi_voice, list):
        vi_voice = vi_voice[0]
    try:
        vi_sentences, ja_sentences = split_vi_ja_sentences(input_text)
        all_sentences = []
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
            except Exception:
                pass

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

async def process_mixed_text_with_google(text: str, ja_voice: str, vi_voice: str):
    vi_sentences, ja_sentences = split_vi_ja_sentences(text)
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
        except Exception:
            pass

    if audio_paths:
        merged_path = os.path.join(output_dir, "merged_output.mp3")
        merge_audio_files(*audio_paths, output_path=merged_path)
        return "✅ Đã tạo file hợp nhất.", merged_path
    else:
        return "❌ Không tạo được file âm thanh.", ""