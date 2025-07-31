# import os
# import re
# import sys
# import asyncio
# import csv
# import shutil
# import datetime
# import hashlib
# import edge_tts
# from pydub import AudioSegment  
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))




# from config.config import (
#     ANKI_MEDIA_DIR,
#     DECK_NAME,
#     VOICE_JA_TTS,
#     VOICE_VI_TTS,
#     OUTPUT_BASE_DIR,
#     FFMPEG_PATH
#     )



# # ==== SETUP IMPORT PATH ====
# from pydub.utils import which
# os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)
# AudioSegment.converter = which("ffmpeg")
# # from API.callAnki import callAnki
# # anki = callAnki(deck_name=DECK_NAME)

# # ==== UTILITIES ====
# def log(message: str, level: str = "INFO"):
#     print(f"[{level.upper()}] {message}")

# def clean_filename(text: str) -> str:
#     text = re.sub(r'[<>:"/\\|?*\n\r\t]', '', text)  
#     text = text.strip().replace(" ", "_").replace(".", "")
#     #text = text.strip()
#     return text

# # ==== TEXT-TO-SPEECH ====
# async def convert_text_to_speech(text: str, voice="ja-JP-KeitaNeural"):
#     """
#     Chuyển đổi văn bản thành giọng nói và lưu vào tệp MP3.

#     Args:
#         text (str): Văn bản cần chuyển đổi.
#         voice (str): Tên giọng đọc (ví dụ: "ja-JP-KeitaNeural", "en-US-JennyNeural").
#         output_path (str): Đường dẫn đầy đủ đến tệp MP3 đầu ra (ví dụ: "outputs/my_audio.mp3").
#         rate (str, optional): Tốc độ giọng đọc (ví dụ: "+50%", "-20%", "medium"). Mặc định là "medium".
#     """
#     try:
#          # Tạo thư mục outputs/mmdd với ngày hiện tại
#         today = datetime.datetime.now().strftime("%m%d")
#         output_dir = f"outputs/{today}"
#         #output_dir = "outputs/test"
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#         # Đặt tên file đầu ra dựa trên input text (loại bỏ ký tự đặc biệt)
#         chars_to_remove = ['.', '。', '!','_', ' ', '　','\n']  # Thêm các ký tự cần loại bỏ
#         text_cleaned_list = [char for char in text if char not in chars_to_remove]
#         safe_text = "".join(text_cleaned_list)
#         output_file = os.path.join(output_dir, f"{safe_text}.mp3")
#         #output_file = os.path.join(output_dir)
#         #print(f"Đang chuyển đổi '{text}' với giọng '{voice}' và tốc độ '{rate}'...")
#         log(f"[DEBUG] generate_audio: voice={voice} ({type(voice)})")
#         if not isinstance(voice, str):
#             raise ValueError("voice must be str")
#         communicator = edge_tts.Communicate(text, voice)
#         await communicator.save(output_file)
       

#         print(f"Đã lưu tệp MP3 thành công tại: {output_file}")
#         return output_file

#     except Exception as e:
#         print(f"Đã xảy ra lỗi khi chuyển đổi văn bản thành giọng nói: {e}")
#         return None
    
# # ==== TEXT-TO-SPEECH ====
# async def convert_text_to_speech2(text: str, voice: str, save_dir: str, filename: str = None):
#     # if not isinstance(voice, str):
#     #     raise ValueError("voice must be str")
#     #log(f"VOICE PARAM: {voice} ({type(voice)})", level="debug")
#     try:
#         os.makedirs(save_dir, exist_ok=True)
#         if not filename:
#             filename = clean_filename(text) + ".mp3"
#         output_path = os.path.join(save_dir, filename)

#         communicator = edge_tts.Communicate(text, voice)
#         await communicator.save(output_path)

#         #log(f"Audio saved: {output_path}")
#         return output_path
#     except Exception as e:
#         log(f"TTS error: {e}")
#         return None

# # ==== AUDIO MERGING ====
# def merge_audio_files(file1: str, file2: str, output_path: str) -> str:
#     try:
#         if not os.path.exists(file1) or not os.path.exists(file2):
#             raise FileNotFoundError("Input audio files not found.")

#         sound1 = AudioSegment.from_file(file1)
#         sound2 = AudioSegment.from_file(file2)

#         combined = sound1 + sound2
#         combined.export(output_path, format="mp3")
#         #log(f"Merged audio saved: {output_path}")
#         return output_path
#     except Exception as e:
#         log(f"Merging error: {e}")
#         return None
    
# # ==== PROCESS CSV AND GENERATE AUDIO ====
# async def process_csv_and_generate_audio(csv_file_path: str) -> list[str]:
#     output_files = []

#     with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile, delimiter=';')
        
#         for i, row in enumerate(reader, start=1):
#             if not row or len(row) < 2:
#                 log(f"❌ Row {i} is empty or has insufficient data.")
#                 continue
            
#             ts = await convert_text_to_speech(text=row[0], voice="ja-JP-KeitaNeural")
#             if not ts:
#                 log(f"❌ TTS failed for row {i}: {row[0]}")
#                 continue

#             file_path = os.path.abspath(ts)
#             file_name = os.path.basename(file_path)
#             dst_path = os.path.join(ANKI_MEDIA_DIR, file_name)

#             try:
#                 shutil.copy(file_path, dst_path)
#                 log(f"📁Copied to: {dst_path}")
#             except Exception as e:
#                 log(f"❌Copied failed: {e}")
#                 continue

#             note = {
#                 "deckName": "TEST1",
#                 "modelName": "Basic",
#                 "fields": {
#                     "Front": row[0],
#                     "Back": row[1],
#                     "Audio 1": f'[sound:{file_name}]'
#                 },
#                 "tags": ["Japanese"]
#             }

#             try:
#                 note_id_list = anki.invoke("findNotes", query=f'note:Basic deck:TEST1 \"Front:{row[0]}\"')
#                 if note_id_list:
#                     note_id = note_id_list[0]
#                     anki.invoke("updateNoteFields", note={
#                         "id": note_id,
#                         "fields": {
#                             "Back": row[1],
#                             "Audio 1": f'[sound:{file_name}]'
#                         }
#                     })
#                     log(f"🔁Updated note: {row[0]}")
#                 else:
#                     anki.invoke("addNote", note=note)
#                     log(f"➕Added new note: {row[0]}")
#             except Exception as e:
#                 log(f"❌ Error at row{i}: {e}")
#                 continue

#             output_files.append(file_path)
#             await asyncio.sleep(1)

#     return output_files



# # async def process_mixed_text(input_text):
# #     """
# #     Process text in the format: [Japanese. Vietnamese]
# #     Converts both parts to speech using appropriate voices.
# #     """
# #     if not input_text.startswith("[") or not input_text.endswith("]"):
# #         print("⚠️ Định dạng không hợp lệ. Text phải nằm trong [ ... ]")
# #         return

# #     try:
# #         content = input_text[1:-1].strip()
# #         parts = [p.strip() for p in content.split('.') if p.strip()]
# #         if len(parts) != 2:
# #             print("⚠️ Không tách được thành 2 phần rõ ràng.")
# #             return

# #         ja_text, vi_text = parts[0], parts[1]
# #         today = datetime.datetime.now().strftime("%m%d")
# #         output_dir = f"outputs/{today}"

# #         ja_voice = "ja-JP-KeitaNeural"
# #         vi_voice = "vi-VN-HoaiMyNeural"

# #         ja_audio = await convert_text_to_speech2(ja_text, ja_voice, output_dir)
# #         vi_audio = await convert_text_to_speech2(vi_text, vi_voice, output_dir)

# #         return {"ja_audio": ja_audio, "vi_audio": vi_audio}

# #     except Exception as e:
# #         print(f"❌ Lỗi xử lý văn bản: {e}")
# #         return None

# # ==== PROCESS MIXED TEXT – STABLE VERSION ====
# async def process_mixed_text(input_text, ja_voice, vi_voice):
#     # if isinstance(ja_voice, list):
#     #     ja_voice = ja_voice[0]
#     # elif not isinstance(ja_voice, str):
#     #     raise ValueError("JA voice must be a string")
#     # if isinstance(vi_voice, list):
#     #     vi_voice = vi_voice[0]
#     # elif not isinstance(vi_voice, str):
#     #     raise ValueError("VN voice must be a string")

#     try:
#         content = input_text.strip()

#         # Tách bằng dấu chấm đầu tiên
#         parts = [p.strip() for p in re.split(r'[。／\.]', content, maxsplit=1)]


#         ja_text = ""
#         vi_text = ""

#         if len(parts) == 1:
#             text = parts[0]
#             if re.search(r'[\u3040-\u30ff\u4e00-\u9faf]', text):
#                 ja_text = text
#             else:
#                 vi_text = text
#         elif len(parts) == 2:
#             ja_text, vi_text = parts

#         today = datetime.datetime.now().strftime("%m%d")
#         output_dir = os.path.join(OUTPUT_BASE_DIR, today)
#         os.makedirs(output_dir, exist_ok=True)

#         output_paths = {}

#         # === Japanese TTS ===
#         if ja_text:
#             ja_audio = await convert_text_to_speech2(ja_text, ja_voice, output_dir)
#             if ja_audio:
#                 output_paths["ja"] = ja_audio
#                 log(f"✅ Japanese audio saved: {ja_audio}")
#             else:
#                 log("❌ Failed to generate Japanese audio.")

#         # === Vietnamese TTS ===
#         if vi_text:
#             vi_hash = hashlib.md5(vi_text.encode("utf-8")).hexdigest()[:6]
#             vi_filename = f"vn_{vi_hash}.mp3"
#             vi_path = os.path.join(output_dir, vi_filename)
#             if os.path.exists(vi_path):
#                 os.remove(vi_path)

#             vi_audio = await convert_text_to_speech2(vi_text, vi_voice, output_dir, vi_filename)
#             if vi_audio:
#                 output_paths["vi"] = vi_audio
#                 log(f"✅ Vietnamese audio saved: {vi_audio}")
#             else:
#                 log("❌ Failed to generate Vietnamese audio.")

            

#         # === Merge nếu có cả hai ===
#         if "ja" in output_paths and "vi" in output_paths:
#             merged_filename = clean_filename(ja_text + "_vn") + "_merged.mp3"
#             merged_path = os.path.join(output_dir, merged_filename)

#             merged_audio = merge_audio_files(output_paths["ja"], output_paths["vi"], merged_path)
#             if merged_audio:
#                 output_paths["merged"] = merged_audio
#                 log(f"✅ Merged audio available at: {merged_audio}")
#             else:
#                 log("❌ Failed to merge audio files.")

#         return output_paths

#     except Exception as e:
#         log(f"❌ Processing error: {e}")
#         return None



# # # ==== MAIN ====
# async def main():
# #     # # Japanese example
#      await process_mixed_text("私は猫が好きです。 Tôi thích mèo", ja_voice=VOICE_JA_TTS[0], vi_voice=VOICE_VI_TTS[0])
# #     # # Vietnamese example
# #     # await convert_text_to_speech_multi("Tôi thích nuôi mèo", lang="vi")
# #     sample_input = "私は猫が好きです. Tôi thích ăn mỳ"
# #     merged_file = await process_mixed_text(sample_input)
# #     if merged_file:
# #         log(f"Final merged audio available at: {merged_file}")
# #     else:
# #         log("❌ Failed to generate merged audio.")

# if __name__ == "__main__":
# #     # csv_file = "F:/Japanese/kaiwa/kaiwa_pv.csv"
# #     # output_files = asyncio.run(process_csv_and_generate_audio(csv_file))
# #     # print(f"\n✅ Processing complete. Total audio files created: {len(output_files)}")
#     asyncio.run(main())

