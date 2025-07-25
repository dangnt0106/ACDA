import gradio as gr
import functions.text_to_speech as tts



demo = gr.Interface(
    fn=tts.text_to_speech, 
    inputs=[gr.Text(label="Text"),],
    outputs=gr.Audio(label="Audio"),
    title="ACDA Chatbot",
    description="Convert Japanese text to speech using Amazon Polly.",)
demo.launch()