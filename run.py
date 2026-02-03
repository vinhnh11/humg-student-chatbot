from ingestion.crawl_quydinh import main as crawl_pdf
from ingestion.ocr_pdf import ocr_all_pdfs
from processing.vector_store import build_vector_store
from rag.qa_chain import build_qa_chain
from app.chatbot_cli import run_chatbot


def show_menu():
    print("""
==============================
 CHỌN CHỨC NĂNG CẦN CHẠY
==============================
1. Crawl & tải PDF quy định
2. OCR toàn bộ PDF
3. Tạo Vector Store
4. Chạy Chatbot RAG
0. Thoát
""")


def main():
    vectorstore = None
    qa_chain = None

    while True:
        show_menu()
        choice = input("Nhập lựa chọn: ").strip()

        if choice == "1":
            print("\n--- ĐANG CRAWL PDF ---")
            crawl_pdf()

        elif choice == "2":
            print("\n--- ĐANG OCR PDF ---")
            documents = ocr_all_pdfs()

        elif choice == "3":
            print("\n--- ĐANG TẠO VECTOR STORE ---")
            documents = ocr_all_pdfs()
            vectorstore = build_vector_store(documents)

        elif choice == "4":
            print("\n--- ĐANG CHẠY CHATBOT ---")
            if vectorstore is None:
                print("⚠ Chưa có vector store → tạo tự động")
                documents = ocr_all_pdfs()
                vectorstore = build_vector_store(documents)

            qa_chain = build_qa_chain(vectorstore)
            run_chatbot(qa_chain)

        elif choice == "0":
            print("Thoát chương trình.")
            break

        else:
            print(" Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
