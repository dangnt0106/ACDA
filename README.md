# ACDA - TTS & Anki Integration

## Mô tả
Dự án này giúp chuyển đổi văn bản tiếng Nhật và tiếng Việt thành file audio, tích hợp với Anki và hỗ trợ giao diện Gradio.

## Yêu cầu hệ thống
- Python >= 3.10
- Windows (đã kiểm thử)
- ffmpeg (đã có sẵn trong thư mục bin)

## Cài đặt
1. Clone dự án:
   ```bash
   git clone https://github.com/dangnt0106/ACDA.git
   ```
2. Cài đặt các thư viện Python:
   ```bash
   pip install -r requirements.txt
   ```

- Có mẫu Dockerfile để build image Python 3.10, cài ffmpeg, copy mã nguồn và chạy Gradio.
- Hướng dẫn build image:
  ```bash
  docker build -t acda-app .
  ```
- Hướng dẫn chạy container:
  ```bash
  docker run -p 7860:7860 acda-app
  ```
- Truy cập giao diện Gradio tại `http://localhost:7860`.

Bạn chỉ cần làm theo README là có thể chạy dự án này trên Docker!
## Chạy giao diện Gradio
```bash
python -m gui.app
```
Hoặc mở file app.py và chạy trực tiếp.

## Sử dụng dòng lệnh
Chạy thử nghiệm chuyển văn bản thành audio:
```bash
python tts/processor.py
```

## Định dạng input
- Mỗi câu tiếng Nhật hoặc tiếng Việt đều được tự động nhận diện và tạo file audio.
- Có thể dùng tiền tố `A:` cho tiếng Nhật, `B:` cho tiếng Việt để chỉ định rõ ngôn ngữ.
- Ví dụ:
  ```
  A:これは日本語のテキストです。
  B:Một chút cũng không biết.
  それよりこれの方がいいですよ。
  Tốt hơn hết là bạn nên thuê một chiếc giường trẻ em thay vì mua nó.
  ```

## Kết quả
- File audio sẽ được lưu trong thư mục `outputs/<ngày tháng>/`.
- File hợp nhất có tên `merged_output.mp3`.

## Lưu ý
- Nếu gặp lỗi về ffmpeg, kiểm tra lại đường dẫn hoặc cài đặt ffmpeg.
- Nếu dùng Anki, cần cấu hình thêm trong anki_integration.

## Liên hệ
- Tác giả: dangnt0106
- Github: https://github.com/dangnt0106/ACDA

---