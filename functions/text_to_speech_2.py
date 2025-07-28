import edge_tts
import asyncio
import os
import datetime
import asyncio
import csv
import shutil

src = r"F:\\Japanese\\kaiwa\\audio\\自己紹介をしてください.mp3"
dst = r"C:\\Users\\ADMIN\\AppData\\Roaming\\Anki2\\Người dùng 1\\collection.media\\自己紹介をしてください.mp3"
shutil.copy(src, dst)

async def convert_text_to_speech(text: str, voice="ja-JP-KeitaNeural"):
    """
    Chuyển đổi văn bản thành giọng nói và lưu vào tệp MP3.

    Args:
        text (str): Văn bản cần chuyển đổi.
        voice (str): Tên giọng đọc (ví dụ: "ja-JP-KeitaNeural", "en-US-JennyNeural").
        output_path (str): Đường dẫn đầy đủ đến tệp MP3 đầu ra (ví dụ: "outputs/my_audio.mp3").
        rate (str, optional): Tốc độ giọng đọc (ví dụ: "+50%", "-20%", "medium"). Mặc định là "medium".
    """
    try:
         # Tạo thư mục outputs/mmdd với ngày hiện tại
        today = datetime.datetime.now().strftime("%m%d")
        output_dir = f"outputs/{today}"
        #output_dir = "outputs/test"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Đặt tên file đầu ra dựa trên input text (loại bỏ ký tự đặc biệt)
        chars_to_remove = ['.', '。', '!','_', ' ', '　','\n']  # Thêm các ký tự cần loại bỏ
        text_cleaned_list = [char for char in text if char not in chars_to_remove]
        safe_text = "".join(text_cleaned_list)
        output_file = os.path.join(output_dir, f"{safe_text}.mp3")
        #output_file = os.path.join(output_dir)
        #print(f"Đang chuyển đổi '{text}' với giọng '{voice}' và tốc độ '{rate}'...")
        communicator = edge_tts.Communicate(text, voice)
        await communicator.save(output_file)
       

        print(f"Đã lưu tệp MP3 thành công tại: {output_file}")
        return output_file

    except Exception as e:
        print(f"Đã xảy ra lỗi khi chuyển đổi văn bản thành giọng nói: {e}")
        return None
# async def main():
#     # Ví dụ 1: Chuyển đổi tiếng Nhật
#     await convert_text_to_speech(
#         text="私は猫を育てるのか好きです",
#         voice="ja-JP-KeitaNeural"
#         )

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

def note_exists(front_text: str, deck_name: str, model_name: str):
    query = f'note:{model_name} deck:{deck_name} "Front:{front_text}"'
    result = invoke("findNotes", query=query)
    return result[0] if result else None

async def main():
    csv_file = "F:/Japanese/kaiwa/kaiwa_pv.csv"
    with open(csv_file, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')   
        for i, row in enumerate(reader, start=1):
            if not row or len(row) < 2:
                #print(f"⚠ Dòng {i} thiếu dữ liệu, bỏ qua.")
                continue

            #print(f"\n=== Dòng {i} | Đang xử lý: {row[0]} ===")
            ts = await convert_text_to_speech(text=row[0], voice="ja-JP-KeitaNeural")
            if not ts:
                #print(f"❌ Lỗi khi chuyển text thành audio dòng {i}")
                continue

            file_path = os.path.abspath(ts)
            file_name = os.path.basename(file_path)

            dst_folder = r"C:\Users\ADMIN\AppData\Roaming\Anki2\Người dùng 1\collection.media"
            dst_path = os.path.join(dst_folder, file_name)

            try:
                shutil.copy(file_path, dst_path)
                print(f"📁: {dst_path}")
            except Exception as e:
                print(f"❌: {e}")
                continue

            note = {
                "deckName": "TEST1",
                "modelName": "Basic",
                "fields": {
                    "Front": row[0],
                    "Back": row[1],
                    "Audio 1": f'[sound:{file_name}]'
                },
                "tags": ["Japanese"]
            }

            try:
                note_id_list = invoke("findNotes", query=f'note:Basic deck:TEST1 "Front:{row[0]}"')
                if note_id_list:
                    note_id = note_id_list[0]
                    invoke("updateNoteFields", note={
                        "id": note_id,
                        "fields": {
                            "Back": row[1],
                            "Audio 1": f'[sound:{file_name}]'
                        }
                    })
                    print(f"🔁: {row[0]}")
                else:
                    invoke("addNote", note=note)
                    print(f"➕: {row[0]}")
            except Exception as e:
                print(f"❌{i}: {e}")
            await asyncio.sleep(1)
    


if __name__ == "__main__":
    asyncio.run(main()) 