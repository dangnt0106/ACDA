import gradio as gr
from tts_engine.processor import process_mixed_text
from config.config import VOICE_JA_TTS, VOICE_VI_TTS
import asyncio


def run_async(text, ja_voice, vi_voice):
    if not isinstance(ja_voice, str) or not isinstance(vi_voice, str):
        return "❌ Voice phải là kiểu chuỗi.", None

    result = asyncio.run(process_mixed_text(text, ja_voice, vi_voice))
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
                        btn = gr.Button("🎧 Tạo Audio")
                        status = gr.Textbox(label="Trạng thái", interactive=False)

                    with gr.Column(scale=3):
                        audio_out = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)
                btn.click(fn=run_async, inputs=[input_text, ja_voice_dropdown, vi_voice_dropdown],
                          outputs=[status, audio_out])
                
            with gr.Tab("Azure"):
                gr.Markdown("### Nhập văn bản để tạo audio (Azure API)")
                with gr.Row():
                    with gr.Column(scale=2):
                        input_text2 = gr.Textbox(label="Nhập văn bản [JA. VI]", lines=4, placeholder="今日は暑いです。 Trời hôm nay nóng quá.")
                        ja_voice_dropdown2 = gr.Dropdown(choices=VOICE_JA_TTS, label="Voice tiếng Nhật", value=VOICE_JA_TTS[0])
                        vi_voice_dropdown2 = gr.Dropdown(choices=VOICE_VI_TTS, label="Voice tiếng Việt", value=VOICE_VI_TTS[0])
                        btn2 = gr.Button("🎧 Tạo Audio")
                        status2 = gr.Textbox(label="Trạng thái", interactive=False)
                    with gr.Column(scale=3):
                        audio_out2 = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)
                btn2.click(fn=run_async, inputs=[input_text2, ja_voice_dropdown2, vi_voice_dropdown2], outputs=[status2, audio_out2])

            with gr.Tab("Google"):
                gr.Markdown("### Nhập văn bản để tạo audio (Google API giả lập)")
                with gr.Row():
                    with gr.Column(scale=2):
                        input_text3 = gr.Textbox(label="Nhập văn bản [JA. VI]", lines=4, placeholder="犬が好きです。 Tôi thích chó.")
                        ja_voice_dropdown3 = gr.Dropdown(choices=VOICE_JA_TTS, label="Voice tiếng Nhật", value=VOICE_JA_TTS[0])
                        vi_voice_dropdown3 = gr.Dropdown(choices=VOICE_VI_TTS, label="Voice tiếng Việt", value=VOICE_VI_TTS[0])
                        btn3 = gr.Button("🎧 Tạo Audio")
                        status3 = gr.Textbox(label="Trạng thái", interactive=False)
                    with gr.Column(scale=3):
                        audio_out3 = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)
                btn3.click(fn=run_async, inputs=[input_text3, ja_voice_dropdown3, vi_voice_dropdown3], outputs=[status3, audio_out3])
    demo.launch()
