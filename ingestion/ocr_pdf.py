from config.settings import PDF_DIR
from pdf2image import convert_from_path
import pytesseract
import os

def ocr_all_pdfs():
    all_text = ""

    pdf_files = [
        PDF_DIR / f
        for f in os.listdir(PDF_DIR)
        if f.lower().endswith(".pdf")
    ]

    for pdf_path in pdf_files:
        pages = convert_from_path(str(pdf_path), dpi=200)
        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page, lang="vie")
            all_text += text + "\n"
            print(f"{pdf_path.name} - Trang {i+1}: {len(text)} ký tự")

    print(f"Tổng số ký tự OCR: {len(all_text)}")
    return all_text
