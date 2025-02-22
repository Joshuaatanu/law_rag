from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from config import Config

def process_constitution():
    loader = PyPDFLoader(Config.PDF_PATH)
    documents = loader.load()
    
    # Extract legal references
    for doc in documents:
        content = doc.page_content
        doc.metadata.update({
            'article': re.findall(r'Article (\d+)', content),
            'section': re.findall(r'SECTION (\d+)', content, re.I),
            'page': doc.metadata['page'] + 1  # PDF pages start at 0
        })
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)


from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL
    )
    return FAISS.from_documents(docs, embeddings)