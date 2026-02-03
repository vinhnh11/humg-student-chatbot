from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from config.settings import LLM_MODEL, GOOGLE_API_KEY
from rag.prompt import qa_prompt

def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0.4,
        max_output_tokens=8192,
        google_api_key=GOOGLE_API_KEY
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=True
    )
