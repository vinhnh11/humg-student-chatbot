from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(all_text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.create_documents([all_text])
