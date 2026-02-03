import pytesseract
from pdf2image import convert_from_path

def ocr_pdf(pdf_path, lang="vie"):
    pages = convert_from_path(pdf_path, dpi=200)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page, lang=lang) + "\n"
    return text
