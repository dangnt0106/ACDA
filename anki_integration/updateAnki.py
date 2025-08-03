import csv
import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from callAnki import request, invoke

# Đọc dữ liệu từ file CSV với dấu phân cách là semicolon
csv_file = r"F:/studyingJapanese/csv/tuvung_0718.csv"

count_update = 0
count_new = 0
count_delete = 0
desk = "TEST1"
tags = ["TUVUNG"]


src = r"F:\\Japanese\\kaiwa\\audio\\自己紹介をしてください.mp3"
dst = r"C:\\Users\\ADMIN\\AppData\\Roaming\\Anki2\\Người dùng 1\\collection.media\\自己紹介をしてください.mp3"
shutil.copy(src, dst)

with open(csv_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if not row or len(row) < 2:
            continue  # Bỏ qua dòng không đủ dữ liệu
        front = row[0]
        back = row[1]
        # Tìm note trong deck 'test1' có Front giống dữ liệu csv
        note_ids = invoke('findNotes', query=f'deck:{desk} Front:"{front}"')
        if note_ids:
            # Nếu tìm thấy, cập nhật trường Back
            for note_id in note_ids:
                update_result = invoke('updateNoteFields', note={
                    'id': note_id,
                    'fields': {'Back': back}
                })
                #print(f"Cập nhật note {note_id}: {front} -> {back}, kết quả: {update_result}")
                count_update += 1
        else:
            # Nếu không tìm thấy, thêm mới note
            note = {
                "deckName": desk,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": tags
            }
            result = invoke("addNote", note=note)
            #print(f"Thêm mới note: {front} -> {back}, kết quả: {result}")
            count_new += 1

print(f"Tổng số note được update: {count_update}")
print(f"Tổng số note thêm mới: {count_new}")
