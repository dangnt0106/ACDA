import pytest
import asyncio
from anki_integration.updateAnki import import_csv_to_anki
from utils.text_utils import split_vi_ja_sentences
from utils.log import log
from utils.hash_utils import short_hash
from utils.file_utils import clean_filename, ensure_output_dir
from utils.audio_utils import merge_audio_files
from tts.processor import process_mixed_text_with_edge, process_mixed_text_with_google
import os

@pytest.mark.asyncio
async def test_process_mixed_text_with_edge():
    text = "私は猫が好きです.Tôi thích mèo"
    ja_voice = "ja-JP-NanamiNeural"
    vi_voice = "vi-VN-PhuongNeural"
    result = await process_mixed_text_with_edge(text, ja_voice, vi_voice)
    assert "merged" in result
    assert os.path.exists(result["merged"])

@pytest.mark.asyncio
async def test_process_mixed_text_with_google():
    text = "私は猫が好きです.Tôi thích mèo"
    ja_voice = "ja"
    vi_voice = "vi"
    status, merged_path = await process_mixed_text_with_google(text, ja_voice, vi_voice)
    assert "Đã tạo file hợp nhất" in status
    assert os.path.exists(merged_path)

def test_split_vi_ja_sentences():
    vi, ja = split_vi_ja_sentences("私は猫が好きです. Tôi thích mèo")
    assert any("mèo" in v for v in vi)
    assert any("猫" in j for j in ja)

def test_log():
    # Chỉ kiểm tra không lỗi khi gọi
    log("Test log", level="debug")

def test_short_hash():
    h = short_hash("test string")
    assert isinstance(h, str) and len(h) == 3

def test_clean_filename():
    s = clean_filename("abc<>:\\|?*\n\r\txyz")
    assert "<" not in s and ":" not in s and "|" not in s

def test_ensure_output_dir():
    path = ensure_output_dir("outputs")
    assert os.path.exists(path)

def test_merge_audio_files():
    # Tạo 2 file audio nhỏ để test
    from pydub.generators import Sine
    sine1 = Sine(440).to_audio_segment(duration=500)
    sine2 = Sine(880).to_audio_segment(duration=500)
    f1 = "outputs/test1.mp3"
    f2 = "outputs/test2.mp3"
    sine1.export(f1, format="mp3")
    sine2.export(f2, format="mp3")
    out = "outputs/test_merged.mp3"
    merge_audio_files(f1, f2, output_path=out)
    assert os.path.exists(out)
    os.remove(f1)
    os.remove(f2)
    os.remove(out)

@pytest.mark.asyncio
async def test_import_csv_to_anki():
    # Tạo file csv nhỏ để test
    test_csv = "outputs/test_anki.csv"
    with open(test_csv, "w", encoding="utf-8") as f:
        f.write("猫;Con mèo\n犬;Con chó\n")
    result = await import_csv_to_anki(test_csv, deck_name="TEST1", tags=["test"], engine="google")
    assert "updated" in result and "added" in result
    os.remove(test_csv)
