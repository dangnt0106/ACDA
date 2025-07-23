import os
from contextlib import closing
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv("F:/Projects/ACDA/API/.env")

def text_to_speech(text, voice_id="Mizuki", rate="medium"):
    """Convert Japanese text to speech using Amazon Polly and save to file with custom rate."""
    polly = boto3.client(
        'polly',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    try:
        # Tạo thư mục outputs nếu chưa tồn tại
        output_dir = "F:/Projects/ACDA/outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Đặt tên file đầu ra dựa trên input text (loại bỏ ký tự đặc biệt)
        safe_text = "".join(c if c.isalnum() else "_" for c in text)
        output_file = os.path.join(output_dir, f"{safe_text}.mp3")
        # Sử dụng SSML để điều chỉnh tốc độ đọc
        ssml_text = f'<speak><prosody rate="{rate}">{text}</prosody></speak>'
        response = polly.synthesize_speech(
            Text=ssml_text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            LanguageCode='ja-JP',
            TextType='ssml'
        )
        with closing(response['AudioStream']) as stream:
            with open(output_file, 'wb') as file:
                file.write(stream.read())
        print(f"Audio saved to {output_file}")
    except ClientError as e:
        print(f"Error synthesizing speech: {e}")

input_text = "最近学んだことは何ですか？"  # Văn bản tiếng Nhật
input_text = input_text.strip() # Loại bỏ dấu câu cuối câu
voice_id = "Mizuki"  # Giọng nữ tiếng Nhật

# Convert text to speech and save as output.mp3 với tốc độ bình thường
text_to_speech(input_text, voice_id, rate="medium")