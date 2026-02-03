def run_chatbot(qa_chain):
    print("Chatbot tư vấn sinh viên HUMG sẵn sàng!")
    print("Nhập 'tạm biệt' để thoát\n")

    chat_history = []

    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() == "tạm biệt":
            break

        result = qa_chain.invoke({
            "question": user_input,
            "chat_history": chat_history
        })

        answer = result["answer"]
        print(f"\nTrợ lý: {answer}\n")
        chat_history.append((user_input, answer))
