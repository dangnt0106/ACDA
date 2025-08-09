import pytest
import asyncio
from anki_integration.updateAnki import import_csv_to_anki
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

@pytest.mark.asyncio
async def test_process_mixed_text_with_google():
    text = "私は猫が好きです.Tôi thích mèo"
    ja_voice = "ja"
    vi_voice = "vi"
    result = await process_mixed_text_with_google(text, ja_voice, vi_voice)
    status, merged_audio_path = result
    assert "Đã tạo file hợp nhất" in status
    assert merged_audio_path.endswith("_merged.mp3")


# @pytest.mark.asyncio
# async def test_import_csv_to_anki():
#     result = await import_csv_to_anki("F:/studyingJapanese/csv/output2.csv", "TEST1", ["N4"], "google")
#     assert result is not None
