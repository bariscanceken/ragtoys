from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os   

load_dotenv()

pdf_folder = "docs"
pdf_paths = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

docs = []
for path in pdf_paths:
    loader = PyPDFLoader(path)
    docs.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)


embedder = OpenAIEmbeddings()

vectorstore = Chroma(
    collection_name="py-chroma",
    persist_directory="./.chroma",
    embedding_function=embedder
)

batch_size = 100 
for i in range(0, len(splits), batch_size):
    batch = splits[i:i+batch_size]
    vectorstore.add_documents(batch)

retriever = vectorstore.as_retriever()
