import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
PDF_DIR = BASE_DIR / "data" / "pdf_downloads"
PDF_DIR.mkdir(parents=True, exist_ok=True)

MAIN_URL = "https://daotaodaihoc.humg.edu.vn/#/quychequydinh"
API_LOC_QUYDINH = "https://daotaodaihoc.humg.edu.vn/api/web/w-locdsquydinh"

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    "AIzaSyB3FtIfwNSi3EbwKEuwK1TKoK5D5PUrkK4"
)

