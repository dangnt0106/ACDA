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
# OUTPUT
OUTPUT_BASE_DIR = "outputs"

# Setup ffmpeg env
PATH=os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")
