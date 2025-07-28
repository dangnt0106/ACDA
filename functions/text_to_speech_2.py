import edge_tts
import asyncio
import os
import datetime
import asyncio




async def convert_text_to_speech(text: str, voice="ja-JP-KeitaNeural"):
    """
    Chuyển đổi văn bản thành giọng nói và lưu vào tệp MP3.

    Args:
        text (str): Văn bản cần chuyển đổi.
        voice (str): Tên giọng đọc (ví dụ: "ja-JP-KeitaNeural", "en-US-JennyNeural").
        output_path (str): Đường dẫn đầy đủ đến tệp MP3 đầu ra (ví dụ: "outputs/my_audio.mp3").
        rate (str, optional): Tốc độ giọng đọc (ví dụ: "+50%", "-20%", "medium"). Mặc định là "medium".
    """
    try:
         # Tạo thư mục outputs/mmdd với ngày hiện tại
        today = datetime.datetime.now().strftime("%m%d")
        output_dir = f"outputs/{today}"
        #output_dir = "outputs/test"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Đặt tên file đầu ra dựa trên input text (loại bỏ ký tự đặc biệt)
        chars_to_remove = ['.', '。', '!','_', ' ', '　','\n']  # Thêm các ký tự cần loại bỏ
        text_cleaned_list = [char for char in text if char not in chars_to_remove]
        safe_text = "".join(text_cleaned_list)
        output_file = os.path.join(output_dir, f"{safe_text}.mp3")
        #output_file = os.path.join(output_dir)
        #print(f"Đang chuyển đổi '{text}' với giọng '{voice}' và tốc độ '{rate}'...")
        communicator = edge_tts.Communicate(text, voice)
        await communicator.save(output_file)
       

        print(f"Đã lưu tệp MP3 thành công tại: {output_file}")
        return output_file

    except Exception as e:
        print(f"Đã xảy ra lỗi khi chuyển đổi văn bản thành giọng nói: {e}")
        return None
async def main():
    # Ví dụ 1: Chuyển đổi tiếng Nhật
    await convert_text_to_speech(
        text="私は猫を育てるのか好きです",
        voice="ja-JP-KeitaNeural"
        )

if __name__ == "__main__":
    asyncio.run(main())