import asyncio
import csv
import shutil
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anki_integration.callAnki import callAnki
from tts.audio_utils import clean_filename
from config.config import ANKI_MEDIA_DIR,DECK_NAME
from tts.processor import (process_mixed_text_with_edge,process_mixed_text_with_google)

# Đọc dữ liệu từ file CSV với dấu phân cách là semicolon
csv_file = r"F:/studyingJapanese/csv/output.csv"

DECK_NAME = "TEST1"
count_update = 0
count_new = 0
count_delete = 0
#desk = "NguPhap_Japanese"
tags = ["N4"]
anki = callAnki(DECK_NAME)

# src = r"F:\\Japanese\\kaiwa\\audio\\自己紹介をしてください.mp3"

# shutil.copy(src, ANKI_MEDIA_DIR)


with open(csv_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if not row or len(row) < 2:            
            continue  # Bỏ qua dòng không đủ dữ liệu
        
        front = clean_filename(row[0])
        back = clean_filename(row[1])        

        # Tạo audio cho front bằng edge_tts
         # --- Tạo file audio bằng edge-tts hoặc google ---
        # Chọn engine: "edge" hoặc "google"
        engine = "goole"
        if engine == "edge":
            result_front = asyncio.run(process_mixed_text_with_edge(front, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural"))
            result_back = asyncio.run(process_mixed_text_with_edge(back, ja_voice="ja-JP-NanamiNeural", vi_voice="vi-VN-PhuongNeural"))
            audio_path_front = result_front.get("merged") or result_front.get("ja") or result_front.get("vi")
            audio_path_back = result_back.get("merged") or result_back.get("ja") or result_back.get("vi")

        else:
            status_front, result_front = asyncio.run(process_mixed_text_with_google(front, ja_voice="ja", vi_voice="vi"))
            status_back, result_back = asyncio.run(process_mixed_text_with_google(back, ja_voice="ja", vi_voice="vi"))
            audio_path_front = result_front
            audio_path_back = result_back
        # Lấy tên file audio để lưu vào trường Audio 1,2
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
        # Tìm note trong deck 'test1' có Front giống dữ liệu csv
        note_ids = anki.invoke('findNotes', query=f'deck:{DECK_NAME} Front:"{front}"')
        if note_ids:
            # Nếu tìm thấy, cập nhật trường Back            
            for note_id in note_ids:
                update_result =anki.invoke('updateNoteFields', note={
                    'id': note_id,
                    'fields': {'Back': back, 'Audio 1': audio_field_front, 'Audio 2': audio_field_back}
                })
                count_update += 1
        else:
            # Nếu không tìm thấy, thêm mới note
            # Kiểm tra lại lần nữa để tránh duplicate do AnkiConnect
            note_ids = anki.invoke('findNotes', query=f'deck:{DECK_NAME} Front:"{front}"')
            if note_ids:
                continue            
            note = {
                    "deckName": DECK_NAME,
                    "modelName": "Basic",
                    "fields": {
                        "Front": front,
                        "Back": back,
                        "Audio 1": audio_field_front,
                        "Audio 2": audio_field_back
                    },
                    "tags": tags
            }
            result = anki.invoke("addNote", note=note)
            count_new += 1

print(f"Tổng số note được update: {count_update}")
print(f"Tổng số note thêm mới: {count_new}")
