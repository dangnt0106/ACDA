import sys, os
import time

# Xóa toàn bộ file audio trong ANKI_MEDIA_DIR sau 10 phút
def delete_audio_files_after_delay(delay_seconds=600):
        print(f"[LOG] Đợi {delay_seconds//60} phút trước khi xóa file audio ở outputs...")
        time.sleep(delay_seconds)
        import datetime
        today = datetime.datetime.now().strftime("%m%d")
        today_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs', today)
        if os.path.exists(today_dir):
            for dirpath, dirnames, filenames in os.walk(today_dir):
                for file in filenames:
                    if file.endswith('.mp3'):
                        file_path = os.path.join(dirpath, file)
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"[LOG] Lỗi khi xóa file {file_path}: {e}")
            print(f"[LOG] Đã xóa toàn bộ file audio trong outputs/{today}.")
        else:
            print(f"[LOG] Không tìm thấy thư mục outputs/{today} để xóa file audio.")