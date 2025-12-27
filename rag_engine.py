import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from vcf_loader import load_vcfs

VECTOR_DB_PATH = "./chroma_db"

def initialize_rag(vcf_directory: str, openai_api_key: str):
    """
    Initializes the RAG pipeline:
    1. Loads VCF data
    2. Creates/Updates Vector Store
    3. Sets up Retrieval Chain
    """
    if not openai_api_key:
        raise ValueError("OpenAI API Key is required.")

    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    # Load Documents
    documents = load_vcfs(vcf_directory)
    if not documents:
        return None, "No VCF files found or parsed in the data directory."

    # Since VCF records are already small chunks, we might not need heavy splitting,
    # but strictly speaking, embedding models have limits.
    # Let's just pass documents directly if they are small enough.
    
    embeddings = OpenAIEmbeddings()
    
    # Initialize Chroma
    vectorstore = Chroma.from_documents(
        documents=documents, 
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    
    # Create Chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    
    return qa_chain, f"Indexed {len(documents)} variants."

def get_answer(chain, question, chat_history):
    result = chain({"question": question, "chat_history": chat_history})
    return result["answer"], result["source_documents"]
