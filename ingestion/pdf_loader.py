import os
from config.settings import PDF_DIR

def load_pdf_paths():
    return [
        os.path.join(PDF_DIR, f)
        for f in os.listdir(PDF_DIR)
        if f.lower().endswith(".pdf")
    ]
