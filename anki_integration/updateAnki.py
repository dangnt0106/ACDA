import asyncio
import csv
import shutil
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anki_integration.callAnki import callAnki
from tts.audio_utils import clean_filename
from config.config import ANKI_MEDIA_DIR
from tts.processor import (process_mixed_text_with_edge, process_mixed_text_with_google)

def import_csv_to_anki(
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
        for row in reader:
            if not row or len(row) < 2:
                continue  # Bỏ qua dòng không đủ dữ liệu

            front = clean_filename(row[0])
            back = clean_filename(row[1])
            if engine == "edge":
                result_front = asyncio.run(process_mixed_text_with_edge(front, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural"))
                result_back = asyncio.run(process_mixed_text_with_edge(back, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural"))
                audio_path_front = result_front.get("merged") or result_front.get("ja") or result_front.get("vi")
                audio_path_back = result_back.get("merged") or result_back.get("ja") or result_back.get("vi")
            else:
                status_front, audio_path_front = asyncio.run(process_mixed_text_with_google(front, ja_voice="ja", vi_voice="vi"))
                status_back, audio_path_back = asyncio.run(process_mixed_text_with_google(back, ja_voice="ja", vi_voice="vi"))

            audio_front = clean_filename(os.path.basename(audio_path_front))
            audio_back = clean_filename(os.path.basename(audio_path_back))
            audio_path = os.path.join(ANKI_MEDIA_DIR, audio_front)
            audio_path_2 = os.path.join(ANKI_MEDIA_DIR, audio_back)

            if not os.path.exists(audio_path):
                shutil.copy(audio_path_front, audio_path)
            if not os.path.exists(audio_path_2):
                shutil.copy(audio_path_back, audio_path_2)

            audio_field_front = f"[sound:{audio_front}]"
            audio_field_back = f"[sound:{audio_back}]"

            note_ids = anki.invoke('findNotes', query=f'deck:{deck_name} Front:"{front}"')
            if note_ids:
                for note_id in note_ids:
                    anki.invoke('updateNoteFields', note={
                        'id': note_id,
                        'fields': {'Back': back, 'Audio 1': audio_field_front, 'Audio 2': audio_field_back}
                    })
                    count_update += 1
            else:
                note_ids = anki.invoke('findNotes', query=f'deck:{deck_name} Front:"{front}"')
                if note_ids:
                    continue
                note = {
                    "deckName": deck_name,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front,
                        "Back": back,
                        "Audio 1": audio_field_front,
                        "Audio 2": audio_field_back
                    },
                    "tags": tags
                }
                anki.invoke("addNote", note=note)
                count_new += 1

    return {"updated": count_update, "added": count_new}

# result = import_csv_to_anki(
#     csv_file=r"F:/studyingJapanese/csv/output2.csv",
#     deck_name="TEST1",
#     tags=["N4"],
#     engine="google"  # hoặc "edge"
# )
# print(result)