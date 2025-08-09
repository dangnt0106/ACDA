import os

# FFMPEG
FFMPEG_PATH = r"F:/Projects/ACDA/ffmpeg/bin/ffmpeg.exe"
FFPROBE_PATH = r"F:/Projects/ACDA/ffmpeg/bin/ffprobe.exe"

# ANKI
ANKI_MEDIA_DIR = r"C:/Users/ADMIN/AppData/Roaming/Anki2/Người dùng 1/collection.media"
DECK_NAME = "TEST1"

# VOICE
VOICE_JA_TTS = [
    "ja-JP-NanamiNeural",
    "ja-JP-KeitaNeural",
    "ja-JP-AoiNeural",
    "ja-JP-DaichiNeural",
]
VOICE_VI_TTS = [
    "vi-VN-HoaiMyNeural",
    "vi-VN-NamMinhNeural"
]
GOOGLE_JA_VOICES = ["ja"]  # Google gTTS chỉ hỗ trợ mã ngôn ngữ, không chọn giọng cụ thể
GOOGLE_VI_VOICES = ["vi"]
# OUTPUT
OUTPUT_BASE_DIR = "outputs"
os.environ["PATH"] += os.pathsep + os.path.abspath("ffmpeg/bin")
# Setup ffmpeg env
os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")
os.environ["PATH"] = os.path.dirname(FFPROBE_PATH) + os.pathsep + os.environ.get("PATH", "")
