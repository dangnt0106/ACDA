import gradio as gr
import asyncio
import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tts.processor import (
    process_mixed_text_with_edge,
    process_mixed_text_with_google,
    preview_mixed_text_with_edge,
    preview_mixed_text_with_google
)
from config.config import VOICE_JA_TTS, VOICE_VI_TTS,GOOGLE_JA_VOICES, GOOGLE_VI_VOICES


def run_async(text, ja_voice, vi_voice):
    if not isinstance(ja_voice, str) or not isinstance(vi_voice, str):
        return "❌ Voice phải là kiểu chuỗi.", None

    result = asyncio.run(process_mixed_text_with_edge(text, ja_voice, vi_voice))
    if not result:
        return "❌ Lỗi xử lý.", None

    audio_file = result.get("merged") or result.get("ja") or result.get("vi")
    return "✅ Thành công!", audio_file


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
                            preview_btn = gr.Button("🔊 Nghe thử (Không lưu)")
                            save_btn = gr.Button("💾 Tạo & Lưu")
                        edge_status = gr.Textbox(label="Trạng thái", interactive=False)

                    with gr.Column(scale=3):
                        edge_audio = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)
                        edge_preview_audio = gr.Audio(label="Preview", type="numpy", interactive=False)

                preview_btn.click(fn=preview_mixed_text_with_edge,
                                inputs=[input_text, ja_voice_dropdown, vi_voice_dropdown],
                                outputs=[edge_status, edge_preview_audio])

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

                        google_preview_btn = gr.Button("🔊 Nghe thử (Không lưu)")
                        google_save_btn = gr.Button("💾 Tạo & Lưu")
                        google_status = gr.Textbox(label="Trạng thái", interactive=False)

                    with gr.Column(scale=3):
                        google_audio = gr.Audio(label="Kết quả Google Audio", type="filepath", interactive=False)
                        google_preview_audio = gr.Audio(label="Preview", type="numpy", interactive=False)

                    google_preview_btn.click(
                        fn=preview_mixed_text_with_google,
                        inputs=[google_input, ja_voice, vi_voice],
                        outputs=[google_status, google_preview_audio]
                    )

                    google_save_btn.click(
                        fn=process_mixed_text_with_google,
                        inputs=[google_input, ja_voice, vi_voice],
                        outputs=[google_status, google_audio]
                    )
    demo.launch()
