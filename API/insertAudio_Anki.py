import json
import urllib.request

import shutil

src = r"F:\\Japanese\\kaiwa\\audio\\自己紹介をしてください.mp3"
dst = r"C:\\Users\\ADMIN\\AppData\\Roaming\\Anki2\\Người dùng 1\\collection.media\\自己紹介をしてください.mp3"
shutil.copy(src, dst)


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

#invoke('createDeck', deck='test1')
##result = invoke('deckNames')
#print('got list of decks: {}'.format(result))

# Lấy danh sách các note IDs trong deck 'kaiwa'
#note_ids = invoke('notesInfo', query='deck:kaiwa')
#print('got list of note IDs: {}'.format(note_ids))

# Lấy danh sách các note IDs có tag 'test'
note_ids = invoke('findNotes', query='tag:test')
print(f"Số thẻ có tag 'test': {len(note_ids)}")
print('Danh sách note IDs:', note_ids)

# Lấy thông tin chi tiết của các note này
if note_ids:
    notes_info = invoke('notesInfo', notes=note_ids)
    for note in notes_info:
        print(json.dumps(note, ensure_ascii=False, indent=2))
        # Cập nhật trường 'Audio 1' với file mp3
        note_id = note['note']['noteId'] if 'note' in note else note['noteId']
        update_fields = {
            'Audio 1': '[sound:自己紹介をしてください.mp3]',
            'Audio 2': '[sound:自己紹介をしてください.mp3]'
        }
        update_result = invoke('updateNoteFields', note={'id': note_id, 'fields': update_fields})
        print(f"Đã cập nhật note {note_id}: {update_result}")
else:
    print("Không có note nào với tag 'test'.")