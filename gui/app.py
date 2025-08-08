import gradio as gr
import asyncio
import sys
import os 
import shutil
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts.processor import (
    process_mixed_text_with_edge,
    process_mixed_text_with_google
)
from config.config import VOICE_JA_TTS, VOICE_VI_TTS,GOOGLE_JA_VOICES, GOOGLE_VI_VOICES
from anki_integration.updateAnki import import_csv_to_anki


def run_async(text, ja_voice, vi_voice):
    if not isinstance(ja_voice, str) or not isinstance(vi_voice, str):
        return "❌ Voice phải là kiểu chuỗi.", None

    result = asyncio.run(process_mixed_text_with_edge(text, ja_voice, vi_voice))
    if not result:
        return "❌ Lỗi xử lý.", None

    audio_file = result.get("merged") or result.get("ja") or result.get("vi")
    return "✅ Thành công!", audio_file

def run_import_anki(csv_file, deck_name, tags, engine, progress=gr.Progress()):
    try:
        import_status = "⏳ Đang xử lý, vui lòng chờ..."
        progress(0, desc=import_status)
        temp_path = "temp_upload.csv"
        shutil.copy(csv_file, temp_path)
        result = import_csv_to_anki(
            csv_file=temp_path,
            deck_name=deck_name,
            tags=tags.split(",") if tags else ["N4"],
            engine=engine
        )
        os.remove(temp_path)
        progress(1, desc="✅ Hoàn thành!")
        return f"Đã cập nhật: {result['updated']}, Thêm mới: {result['added']}"
    except Exception as e:
        progress(1, desc="❌ Lỗi!")
        print(f"Error: {e}")
        return f"❌ Đã xảy ra lỗi: {str(e)}"


def launch_gui():
    with gr.Blocks() as demo:
        gr.Markdown("## 🎙️ Text-to-Speech: Japanese & Vietnamese")

        with gr.Tabs():
            with gr.Tab("Edge TTS"):
                gr.Markdown("### Nhập văn bản để tạo audio")
                with gr.Row():
                    with gr.Column(scale=2):
                        input_text = gr.Textbox(label="Nhập văn bản [JA. VI]", lines=4,
                                                placeholder="私は猫が好きです. Tôi thích mèo")
                        ja_voice_dropdown = gr.Dropdown(choices=VOICE_JA_TTS, label="Voice tiếng Nhật",
                                                        value=VOICE_JA_TTS[0])
                        vi_voice_dropdown = gr.Dropdown(choices=VOICE_VI_TTS, label="Voice tiếng Việt",
                                                        value=VOICE_VI_TTS[0])
                        with gr.Row():                            
                            save_btn = gr.Button("💾 Tạo & Lưu")
                        edge_status = gr.Textbox(label="Trạng thái", interactive=False)

                    with gr.Column(scale=3):
                        edge_audio = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)                   

                save_btn.click(fn=run_async,
                            inputs=[input_text, ja_voice_dropdown, vi_voice_dropdown],
                            outputs=[edge_status, edge_audio])

            with gr.Tab("Google"):
                gr.Markdown("### TTS bằng Google gTTS (miễn phí)")
                with gr.Row():
                    with gr.Column(scale=2):
                        google_input = gr.Textbox(label="Nhập văn bản", lines=4)
                        ja_voice = gr.Dropdown(GOOGLE_JA_VOICES, value="ja", label="Voice Japanese (Google)")
                        vi_voice = gr.Dropdown(GOOGLE_VI_VOICES, value="vi", label="Voice Vietnamese (Google)")

                       
                        google_save_btn = gr.Button("💾 Tạo & Lưu")
                        google_status = gr.Textbox(label="Trạng thái", interactive=False)

                    with gr.Column(scale=3):
                        google_audio = gr.Audio(label="Kết quả Google Audio", type="filepath", interactive=False)      

                    google_save_btn.click(
                        fn=process_mixed_text_with_google,
                        inputs=[google_input, ja_voice, vi_voice],
                        outputs=[google_status, google_audio]
                    )
            with gr.Tab("Update Anki từ CSV"):
                gr.Markdown("### Import CSV vào Anki (có audio)")
                with gr.Row():
                    csv_file = gr.File(label="Chọn file CSV", file_types=[".csv"])
                    deck_name = gr.Textbox(label="Tên bộ thẻ (deck)", value="TEST1")
                    tags = gr.Textbox(label="Tags (phân cách bằng dấu phẩy)", value="TuVung")
                    engine = gr.Dropdown(choices=["google", "edge"], value="google", label="Engine TTS")
                import_btn = gr.Button("Import vào Anki")
                import_status = gr.Textbox(label="Kết quả", interactive=False)

                import_btn.click(
                    fn=run_import_anki,
                    inputs=[csv_file, deck_name, tags, engine],
                    outputs=import_status,
                    show_progress=True
                )
    demo.launch()
