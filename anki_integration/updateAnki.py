import csv
import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# Đọc dữ liệu từ file CSV với dấu phân cách là semicolon
csv_file = r"F:\studyingJapanese\csv\NguPhapN4_VD.csv"

count_update = 0
count_new = 0
count_delete = 0
desk = "NguPhap_Japanese"
tags = ["N4", "grammar"]


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
