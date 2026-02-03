import asyncio

from ingestion.crawl_quy_dinh import main as crawl_quy_dinh_main
from ingestion.ocr_pdf import ocr_all_pdfs
from processing.text_splitter import split_text
from processing.embedding_store import build_vectorstore
from rag.qa_chain import create_qa_chain
from app.chatbot_cli import run_chatbot


def run_menu():
    vectorstore = None

    while True:
        print("""

 MENU CHATBOT HUMG

1. Crawl quy chế – quy định
2. Chạy chatbot tư vấn
0. Thoát

""")
        choice = input("Chọn chức năng: ").strip()
        if choice == "1":
            print("\n ĐANG CRAWL QUY CHẾ – QUY ĐỊNH...\n")
            asyncio.run(crawl_quy_dinh_main())
            print("\n Hoàn tất crawl\n")

        elif choice == "2":
            print("\n KHỞI ĐỘNG CHATBOT\n")

            print("OCR tài liệu PDF...")
            all_text = ocr_all_pdfs()

            print("Chia nhỏ văn bản...")
            docs = split_text(all_text)

            print("Tạo Vector Database (FAISS)...")
            vectorstore = build_vectorstore(docs)
            print(" Vector Database đã sẵn sàng\n")

            qa_chain = create_qa_chain(vectorstore)
            run_chatbot(qa_chain)

        elif choice == "0":
            print("Thoát chương trình.")
            break

        else:
            print(" Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    run_menu()
