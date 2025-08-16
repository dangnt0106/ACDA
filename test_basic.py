import pytest
import asyncio
from anki_integration.updateAnki import import_csv_to_anki
from tts.audio_utils import split_vi_ja_sentences
from tts.processor import process_mixed_text_with_edge,process_mixed_text_with_google

@pytest.mark.asyncio
async def test_process_mixed_text_with_edge():
    text = "私は猫が好きです.Tôi thích mèo"
    ja_voice = "ja-JP-NanamiNeural"
    vi_voice = "vi-VN-PhuongNeural"
    result = await process_mixed_text_with_edge(text, ja_voice, vi_voice)
    assert "ja" in result
    # hoặc kiểm tra có ít nhất 1 key
    assert any(k in result for k in ("ja", "vi"))

