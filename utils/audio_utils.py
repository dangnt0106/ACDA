from pydub import AudioSegment

def merge_audio_files(*audio_paths, output_path):
    """Gộp nhiều file audio thành một file mp3."""
    merged = None
    for path in audio_paths:
        audio = AudioSegment.from_file(path)
        if merged is None:
            merged = audio
        else:
            merged += audio
    if merged:
        merged.export(output_path, format="mp3")
        return output_path
    return None
