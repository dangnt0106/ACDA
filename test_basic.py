import pytest
import asyncio
from anki_integration.updateAnki import import_csv_to_anki
from utils.text_utils import split_vi_ja_sentences
from utils.log import log
from utils.hash_utils import short_hash
from utils.file_utils import clean_filename, ensure_output_dir
from utils.audio_utils import merge_audio_files
import os

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
