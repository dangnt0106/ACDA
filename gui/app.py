import gradio as gr
import asyncio
import functions.text_to_speech_2 as tts

# Wrapper chạy async function
def run_async(text):
    result = asyncio.run(tts.process_mixed_text(text))
    if not result:
        return "❌ Lỗi xử lý.", None

    audio_file = result.get("merged") or result.get("ja") or result.get("vi")
    return "✅ Thành công!" if audio_file else "⚠️ Không có file audio.", audio_file
def launch_gui():
# Giao diện nằm ngang
    with gr.Blocks() as demo:
        gr.Markdown("## 🎙️ Text-to-Speech: Japanese & Vietnamese")

        with gr.Row():
            with gr.Column(scale=2):
                input_text = gr.Textbox(label="Nhập văn bản [JA. VI]", lines=4, placeholder="私は猫が好きです. Tôi thích mèo")
                btn = gr.Button("🎧 Tạo Audio")
                status = gr.Textbox(label="Trạng thái", interactive=False)

            with gr.Column(scale=3):
                audio_out = gr.Audio(label="Kết quả Audio", type="filepath", interactive=False)

        btn.click(fn=run_async, inputs=input_text, outputs=[status, audio_out])

    demo.launch()

