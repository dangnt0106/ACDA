import re

def split_vi_ja_sentences(text: str) -> tuple[list[str], list[str]]:
    """Tách câu tiếng Việt và tiếng Nhật từ text."""
    ja_pattern = r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9faf]'
    vi_pattern = r'[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸỳỵỷỹ]'
    sentences = re.split(r'([.。?!？\n\r])', text)
    merged_sentences = []
    buf = ''
    for part in sentences:
        if part in ['.', '。', '?', '！', '!', '？', '\n', '\r']:
            buf += part
            merged_sentences.append(buf.strip())
            buf = ''
        else:
            buf += part
    if buf.strip():
        merged_sentences.append(buf.strip())
    vi_sentences = []
    ja_sentences = []
    for s in merged_sentences:
        s = s.strip()
        if not s:
            continue
        if re.search(ja_pattern, s):
            ja_sentences.append(s)
        elif re.search(vi_pattern, s):
            vi_sentences.append(s)
    return vi_sentences, ja_sentences
