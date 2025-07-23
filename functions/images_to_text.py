from anyio import sleep
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
from PIL import Image
import glob
import os

# Đảm bảo đã cài đặt Tesseract và các gói ngôn ngữ: jpn, vie
# pip install pytesseract pillow

def extract_text_tesseract(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='jpn+vie')
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""

image_folder = r"F:\\Projects\\ACDA\\images\\"
image_files = glob.glob(os.path.join(image_folder, "*.png")) + glob.glob(os.path.join(image_folder, "*.jpg"))

print(f"Found {len(image_files)} image files.")

for image_path in image_files:
    print(f"Extracting text from: {image_path}")
    text = extract_text_tesseract(image_path)
    print("Extracted text:")
    print(text)
    text=text.replace("\n", " ").replace("\r", "")
    print("-" * 40)
    image_path = os.path.splitext(image_path)[0]  # Remove file extension
    # Save the extracted text to a .txt file with the same name as the image    
    output_path = image_path + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
