from ingestion.pdf_loader import load_pdf_paths
from ingestion.ocr_processor import ocr_pdf
from processing.text_splitter import split_text
from processing.vector_store import build_vectorstore
from rag.qa_chain import build_qa_chain

def main():
    all_text = ""
    for pdf in load_pdf_paths():
        all_text += ocr_pdf(pdf)

    docs = split_text(all_text)
    vectorstore = build_vectorstore(docs)
    qa_chain = build_qa_chain(vectorstore)

    chat_history = []

    print("Chatbot HUMG sẵn sàng!")

    while True:
        q = input("Bạn: ")
        if q.lower() == "tạm biệt":
            break

        result = qa_chain.invoke({
            "question": q,
            "chat_history": chat_history
        })

        print("Trợ lý:", result["answer"])
        chat_history.append((q, result["answer"]))

if __name__ == "__main__":
    main()
