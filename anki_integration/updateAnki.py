import csv
import shutil
import os
from anki_integration.callAnki import callAnki
from utils.file_utils import clean_filename
from utils.hash_utils import short_hash
from config.config import ANKI_MEDIA_DIR
from tts.processor import (process_mixed_text_with_edge, process_mixed_text_with_google)

async def import_csv_to_anki(
    csv_file: str,
    deck_name: str = "TEST1",
    tags: list = ["N4"],
    engine: str = "google"
):
    count_update = 0
    count_new = 0
    anki = callAnki(deck_name)

    with open(csv_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for idx, row in enumerate(reader):
            if not row or len(row) < 1:
                continue

            jp_word = clean_filename(row[0])
            vi_meaning = clean_filename(row[1]) if len(row) > 1 else ""



            # Tạo audio cho từng từ/câu tiếng Nhật (Audio 1)
            audio_filename_1 = f"jp_{short_hash(jp_word)}.mp3"
            audio_path_1 = None
            if engine == "edge":
                result_1 = await process_mixed_text_with_edge(jp_word, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural")
                audio_path_candidate_1 = os.path.join(os.path.dirname(result_1.get("merged")), audio_filename_1)
                if os.path.exists(audio_path_candidate_1):
                    audio_path_1 = audio_path_candidate_1
                else:
                    if result_1.get("jp_1.mp3"):
                        src_path_1 = os.path.join(os.path.dirname(result_1.get("merged")), "jp_1.mp3")
                        shutil.copy(src_path_1, audio_path_candidate_1)
                        audio_path_1 = audio_path_candidate_1
            else:
                status_1, temp_audio_path_1 = await process_mixed_text_with_google(jp_word, ja_voice="ja", vi_voice="vi")
                audio_path_candidate_1 = os.path.join(os.path.dirname(temp_audio_path_1), audio_filename_1)
                if os.path.exists(audio_path_candidate_1):
                    audio_path_1 = audio_path_candidate_1
                else:
                    jp_path_1 = os.path.join(os.path.dirname(temp_audio_path_1), "jp_1.mp3")
                    if os.path.exists(jp_path_1):
                        shutil.copy(jp_path_1, audio_path_candidate_1)
                        audio_path_1 = audio_path_candidate_1

            if not audio_path_1 or not os.path.exists(audio_path_1):
                continue

            audio_file_1 = clean_filename(os.path.basename(audio_path_1))
            audio_dest_1 = os.path.join(ANKI_MEDIA_DIR, audio_file_1)
            if audio_path_1 != audio_dest_1:
                if audio_path_1 and audio_dest_1 and os.path.abspath(audio_path_1) != os.path.abspath(audio_dest_1):
                    shutil.copy(audio_path_1, audio_dest_1)

            audio_field_1 = f"[sound:{audio_file_1}]"

            # Tạo audio cho từng dòng cột B (Audio 2, đúng thứ tự)
            audio_field_2 = ""
            if vi_meaning:
                audio_filename_2 = f"vi_ja_{short_hash(vi_meaning)}.mp3"
                audio_path_2 = None
                if engine == "edge":
                    # Synthesize cả tiếng Nhật và tiếng Việt cho Audio 2
                    result_2 = await process_mixed_text_with_edge(vi_meaning, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural")
                    vi_path = result_2.get("vi_1.mp3")
                    jp_path = result_2.get("jp_1.mp3")
                    audio_paths = [p for p in [jp_path, vi_path] if p and os.path.exists(p)]
                    audio_path_2 = os.path.join(os.path.dirname(result_2.get("merged")), audio_filename_2)
                    if audio_paths:
                        from utils.audio_utils import merge_audio_files
                        merge_audio_files(*audio_paths, output_path=audio_path_2)
                else:
                    # Synthesize cả tiếng Nhật và tiếng Việt cho Audio 2
                    status_2, temp_audio_path_2 = await process_mixed_text_with_google(vi_meaning, ja_voice="ja", vi_voice="vi")
                    vi_path = os.path.join(os.path.dirname(temp_audio_path_2), "vi_1.mp3")
                    jp_path = os.path.join(os.path.dirname(temp_audio_path_2), "jp_1.mp3")
                    audio_paths = [p for p in [jp_path, vi_path] if os.path.exists(p)]
                    audio_path_2 = os.path.join(os.path.dirname(temp_audio_path_2), audio_filename_2)
                    if audio_paths:
                        from utils.audio_utils import merge_audio_files
                        merge_audio_files(*audio_paths, output_path=audio_path_2)

                if audio_path_2 and os.path.exists(audio_path_2):
                    audio_file_2 = clean_filename(os.path.basename(audio_path_2))
                    audio_dest_2 = os.path.join(ANKI_MEDIA_DIR, audio_file_2)
                    if audio_path_2 != audio_dest_2:
                        if audio_path_2 and audio_dest_2 and os.path.abspath(audio_path_2) != os.path.abspath(audio_dest_2):
                            shutil.copy(audio_path_2, audio_dest_2)
                    audio_field_2 = f"[sound:{audio_file_2}]"

            note_ids = anki.invoke('findNotes', query=f'deck:{deck_name} Front:"{jp_word}"')
            if note_ids:
                for note_id in note_ids:
                    anki.invoke('updateNoteFields', note={
                        'id': note_id,
                        'fields': {'Back': vi_meaning, 'Audio 1': audio_field_1, 'Audio 2': audio_field_2}
                    })
                    count_update += 1
            else:
                note_ids = anki.invoke('findNotes', query=f'deck:{deck_name} Front:"{jp_word}"')
                if note_ids:
                    continue
                note = {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": jp_word,
                        "Back": vi_meaning,
                        "Audio 1": audio_field_1,
                        "Audio 2": audio_field_2
                    },
                    "tags": tags
                }
                try:
                    anki.invoke("addNote", note=note)
                except Exception as e:
                    if "duplicate" in str(e):
                        continue
                    else:
                        raise
                count_new += 1
    return {"updated": count_update, "added": count_new}