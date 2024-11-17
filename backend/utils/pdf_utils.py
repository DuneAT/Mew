import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
import requests
from backend.utils.db_utils import store_embedding_in_postgres
from backend.utils.constants import serverConstants, postgreSQLConstants

# Functions to process PDF files


def extract_text_from_pdf(file_path):
    """
    Extracts text from each page of a PDF file using pdfplumber.
    """
    text_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text_pages.append((text, page_number))
    return text_pages


def chunk_text_by_page(text_pages, chunk_size=1024):
    """
    Splits text from each page into chunks.
    """
    all_chunks = []
    for text, page_number in text_pages:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size)
        chunks = splitter.split_text(text)
        all_chunks.extend((chunk, page_number) for chunk in chunks)
    return all_chunks


def embed_text(text):
    """
    Embeds text using the Meta-Llama model.

    Args:
        text (str): The text to embed.

    Returns:
        list: The embedding vector.
    """
    data = {
        "model": serverConstants.embedding_model,
        "prompt": text
    }
    response = requests.post(serverConstants.url_embedding, json=data)
    embedding = response.json()
    return embedding


def chunk_and_embed_file_and_store(file_path, chunk_size=1024):
    """
    Extracts text from a PDF, splits it into chunks, embeds each chunk, and stores in a PostgreSQL database.

    Args:
        file_path (str): The path to the PDF file to process.
        chunk_size (int): The size of each chunk in characters.
    """
    text_pages = extract_text_from_pdf(file_path)
    chunks = chunk_text_by_page(text_pages, chunk_size)
    file_name = Path(file_path).name
    for i, (chunk, page) in enumerate(chunks):
        embedding = embed_text(chunk)
        store_embedding_in_postgres(file_name, chunk, embedding, i, page)
