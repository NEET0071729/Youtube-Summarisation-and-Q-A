from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

import os
from dotenv import load_dotenv
load_dotenv()

def process_youtube_url(video_url: str):
    # Initialize loader with minimal settings[cite: 1]
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    docs = loader.load()

    # splitting Documents[cite: 1]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 80)
    splited_text = text_splitter.split_documents(docs)

    # Indexing and Embedding initialising[cite: 1]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma.from_documents(splited_text, embedding=embeddings, persist_directory="./data/chroma_db")
    
    return True