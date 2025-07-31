import os
from contextlib import closing
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import datetime

# Load biến môi trường từ file .env
load_dotenv("F:/Projects/ACDA/API/.env")

def text_to_speech(text, voice_id="Takumi", rate="medium"):
    """Convert Japanese text to speech using Amazon Polly and save to file with custom rate."""
    polly = boto3.client(
        'polly',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION")
    )
    try:
         # Tạo thư mục outputs/mmdd với ngày hiện tại
        today = datetime.datetime.now().strftime("%m%d")
        output_dir = f"F:/Projects/ACDA/outputs/{today}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Đặt tên file đầu ra dựa trên input text (loại bỏ ký tự đặc biệt)
        chars_to_remove = ['.', '。', '!','_', ' ', '　','\n']  # Thêm các ký tự cần loại bỏ
        text_cleaned_list = [char for char in text if char not in chars_to_remove]
        safe_text = "".join(text_cleaned_list)
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
    return output_file

# input_text = "この車の諸元表を見せてください。"  # Văn bản tiếng Nhật

# voice_id = "Takumi" 
# # chars_to_remove = ['.', '。', '!']
# # text_cleaned_list = [char for char in input_text if char not in chars_to_remove]

# # final_text = "".join(text_cleaned_list)
# #print(f"Sử dụng list comprehension: {final_text}")

# # Convert text to speech and save as output.mp3 với tốc độ bình thường
# text_to_speech(input_text, voice_id, rate="100%")  # Tốc độ bình thường