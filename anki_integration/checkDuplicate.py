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

# Đọc dữ liệu từ file CSV
csv_file = r"F:\studyingJapanese\csv\NguPhapN5_VD.csv"
with open(csv_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if not row or len(row) < 2:
            continue  # Bỏ qua dòng không đủ dữ liệu
        front = row[0]
        back = row[1]
        # Kiểm tra note đã tồn tại trong deck "NguPhap_Japanese"
        note_ids = invoke('findNotes', query=f'deck:NguPhap_Japanese Front:"{front}"')
        if note_ids:
            print(f"Data bị trùng: Front='{front}', Back='{back}'")