import hashlib

def short_hash(text: str) -> str:
    """Tạo mã hash ngắn cho text (3 ký tự đầu)."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:3]
