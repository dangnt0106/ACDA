import os
import re
import sys
import asyncio
import csv
import shutil
import datetime
import hashlib
from pydub import AudioSegment
from pydub.utils import which
import edge_tts

# ==== CONFIGURATION ====
# Add ffmpeg path to system PATH at runtime

FFMPEG_PATH = r"F:/Projects/ACDA/ffmpeg/bin/ffmpeg.exe"
FFPROBE_PATH = r"F:/Projects/ACDA/ffmpeg/bin/ffprobe.exe"
ANKI_MEDIA_DIR = r"C:/Users/ADMIN/AppData/Roaming/Anki2/Người dùng 1/collection.media"
DECK_NAME = "TEST1"
VOICE_JA = "ja-JP-KeitaNeural"
VOICE_VI = "vi-VN-HoaiMyNeural"
OUTPUT_BASE_DIR = "outputs"

# ==== SETUP FFMPEG ====
AudioSegment.converter = FFMPEG_PATH
AudioSegment.ffprobe = FFPROBE_PATH

# ==== SETUP IMPORT PATH ====
ffmpeg_dir = r"ffmpeg/bin"
os.environ["PATH"] += os.pathsep + ffmpeg_dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from API.callAnki import callAnki
anki = callAnki(deck_name=DECK_NAME)

# ==== UTILITIES ====
def log(message: str):
    print(f"[LOG] {message}")

def clean_filename(text: str, fallback: str = "audio") -> str:
    cleaned = re.sub(r'[\/*?:"<>|\s。.!]', '', text)
    #h = hashlib.md5(text.encode("utf-8")).hexdigest()[:6]
    return f"{cleaned}" if cleaned else fallback

# ==== TEXT-TO-SPEECH ====
async def convert_text_to_speech(text: str, voice: str, save_dir: str) -> str:
    try:
        os.makedirs(save_dir, exist_ok=True)
        filename = clean_filename(text) + ".mp3"
        output_path = os.path.join(save_dir, filename)

        communicator = edge_tts.Communicate(text, voice)
        await communicator.save(output_path)

        log(f"Audio saved: {output_path}")
        return output_path
    except Exception as e:
        log(f"TTS error: {e}")
        return None

# ==== AUDIO MERGING ====
def merge_audio_files(file1: str, file2: str, output_path: str) -> str:
    try:
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise FileNotFoundError("Input audio files not found.")

        sound1 = AudioSegment.from_file(file1)
        sound2 = AudioSegment.from_file(file2)

        combined = sound1 + sound2
        combined.export(output_path, format="mp3")
        log(f"Merged audio saved: {output_path}")
        return output_path
    except Exception as e:
        log(f"Merging error: {e}")
        return None
    
# ==== PROCESS CSV AND GENERATE AUDIO ====
async def process_csv_and_generate_audio(csv_file_path: str) -> list[str]:
    output_files = []

    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        for i, row in enumerate(reader, start=1):
            if not row or len(row) < 2:
                log(f"❌ Row {i} is empty or has insufficient data.")
                continue
            
            ts = await convert_text_to_speech(text=row[0], voice="ja-JP-KeitaNeural")
            if not ts:
                log(f"❌ TTS failed for row {i}: {row[0]}")
                continue

            file_path = os.path.abspath(ts)
            file_name = os.path.basename(file_path)
            dst_path = os.path.join(ANKI_MEDIA_DIR, file_name)

            try:
                shutil.copy(file_path, dst_path)
                log(f"📁Copied to: {dst_path}")
            except Exception as e:
                log(f"❌Copied failed: {e}")
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
                note_id_list = anki.invoke("findNotes", query=f'note:Basic deck:TEST1 \"Front:{row[0]}\"')
                if note_id_list:
                    note_id = note_id_list[0]
                    anki.invoke("updateNoteFields", note={
                        "id": note_id,
                        "fields": {
                            "Back": row[1],
                            "Audio 1": f'[sound:{file_name}]'
                        }
                    })
                    log(f"🔁Updated note: {row[0]}")
                else:
                    anki.invoke("addNote", note=note)
                    log(f"➕Added new note: {row[0]}")
            except Exception as e:
                log(f"❌ Error at row{i}: {e}")
                continue

            output_files.append(file_path)
            await asyncio.sleep(1)

    return output_files



async def process_mixed_text(input_text: str):
    """
    Process text in the format: [Japanese. Vietnamese]
    Converts both parts to speech using appropriate voices.
    """
    if not input_text.startswith("[") or not input_text.endswith("]"):
        print("⚠️ Định dạng không hợp lệ. Text phải nằm trong [ ... ]")
        return

    try:
        content = input_text[1:-1].strip()
        parts = [p.strip() for p in content.split('.') if p.strip()]
        if len(parts) != 2:
            print("⚠️ Không tách được thành 2 phần rõ ràng.")
            return

        ja_text, vi_text = parts[0], parts[1]
        today = datetime.datetime.now().strftime("%m%d")
        output_dir = f"outputs/{today}"

        ja_voice = "ja-JP-KeitaNeural"
        vi_voice = "vi-VN-HoaiMyNeural"

        ja_audio = await convert_text_to_speech(ja_text, ja_voice, output_dir)
        vi_audio = await convert_text_to_speech(vi_text, vi_voice, output_dir)

        return {"ja_audio": ja_audio, "vi_audio": vi_audio}

    except Exception as e:
        print(f"❌ Lỗi xử lý văn bản: {e}")
        return None

# ==== PROCESS MIXED TEXT – STABLE VERSION ====
async def process_mixed_text(input_text: str):
    try:
        # Remove [ ] if present
        if input_text.startswith("[") and input_text.endswith("]"):
            content = input_text[1:-1].strip()
        else:
            content = input_text.strip()

        # Split by first period
        parts = [p.strip() for p in content.split('.', maxsplit=1)]
        if len(parts) != 2:
            log("⚠️ Failed to split input into two parts.")
            return None

        ja_text, vi_text = parts
        today = datetime.datetime.now().strftime("%m%d")
        output_dir = os.path.join(OUTPUT_BASE_DIR, today)
        os.makedirs(output_dir, exist_ok=True)

        # === Generate Japanese audio ===
        ja_audio = await convert_text_to_speech(ja_text, VOICE_JA, output_dir)
        if not ja_audio or not os.path.isfile(ja_audio):
            log("❌ Failed to generate Japanese audio.")
            return None

        # === Generate Vietnamese audio ===
        vi_hash = hashlib.md5(vi_text.encode("utf-8")).hexdigest()[:6]
        vi_filename = f"vn_{vi_hash}.mp3"
        vi_path = os.path.join(output_dir, vi_filename)

        if os.path.exists(vi_path):
            os.remove(vi_path)

        try:
            communicator = edge_tts.Communicate(vi_text, VOICE_VI)
            await communicator.save(vi_path)
            log(f"✅ Vietnamese audio saved: {vi_path}")
        except Exception as e:
            log(f"❌ Vietnamese TTS error: {e}")
            return None

        if not os.path.exists(vi_path):
            log("❌ Vietnamese audio file not found after saving.")
            return None

        # === Merge both ===
        merged_filename = clean_filename(ja_text + "_vn") + "_merged.mp3"
        merged_path = os.path.join(output_dir, merged_filename)

        merged_audio = merge_audio_files(ja_audio, vi_path, merged_path)
        if merged_audio:
            log(f"✅ Final merged audio available at: {merged_audio}")
            return merged_audio
        else:
            log("❌ Failed to merge audio files.")
            return None

    except Exception as e:
        log(f"❌ Processing error: {e}")
        return None




# ==== MAIN ====
async def main():
    # # Japanese example
    # await convert_text_to_speech_multi("私は猫が好きです. Tôi thích nuôi mèo", lang="ja+vi")
    # # Vietnamese example
    # await convert_text_to_speech_multi("Tôi thích nuôi mèo", lang="vi")
    sample_input = "私は猫が好きです. Tôi thích ăn mỳ"
    merged_file = await process_mixed_text(sample_input)
    if merged_file:
        log(f"Final merged audio available at: {merged_file}")
    else:
        log("❌ Failed to generate merged audio.")

if __name__ == "__main__":
    # csv_file = "F:/Japanese/kaiwa/kaiwa_pv.csv"
    # output_files = asyncio.run(process_csv_and_generate_audio(csv_file))
    # print(f"\n✅ Processing complete. Total audio files created: {len(output_files)}")
    asyncio.run(main())
