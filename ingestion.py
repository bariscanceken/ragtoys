from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from bs4 import BeautifulSoup
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
import os   

load_dotenv()

pdf_folder = "docs"
pdf_paths = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
docs = [PyPDFLoader(path).load() for path in pdf_paths]

docs_list = [doc.page_content for sublist in docs for doc in sublist]


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size = 3000 , chunk_overlap = 300
)

splits = text_splitter.create_documents(docs_list)

embedder = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=splits,
    collection_name="py-chroma",
    persist_directory="./.chroma",
    embedding=embedder
)

retriever = Chroma(
    collection_name="py-chroma",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="./.chroma"
).as_retriever()