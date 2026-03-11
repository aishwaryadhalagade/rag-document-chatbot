from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_store(pdf_path):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    # Add metadata source to each chunk
    for doc in docs:
        doc.metadata["source"] = pdf_path

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local("faiss_index")

    return vectorstore