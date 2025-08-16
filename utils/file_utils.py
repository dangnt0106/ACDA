import os
import re
import datetime

def clean_filename(text: str) -> str:
    """Làm sạch tên file khỏi ký tự đặc biệt."""
    return re.sub(r'[<>:"\\|?*\n\r\t]', '', text)

def ensure_output_dir(path: str):
    """Tạo thư mục output theo ngày hiện tại."""
    today = datetime.datetime.now().strftime("%m%d")
    out_dir = os.path.join(path, today)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir
