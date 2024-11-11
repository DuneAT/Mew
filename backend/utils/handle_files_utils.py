import json
import requests
import psycopg2
import pdfplumber
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

from backend.utils.constants import serverConstants, postgreSQLConstants

db_config = postgreSQLConstants.db_config


def store_embedding_in_postgres(file_name, chunk_text, embedding, chunk_number, page):
    try:
        # Ensure embedding is a list by extracting if necessary
        if isinstance(embedding, dict) and "embedding" in embedding:
            embedding = embedding["embedding"]

        # Establish connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Begin a transaction
        conn.autocommit = False  # Disable auto-commit for transaction safety

        # Insert file into files table if it doesn't exist
        cursor.execute("""
            INSERT INTO files (file_name, created_at)
            VALUES (%s, %s)
            ON CONFLICT (file_name) DO NOTHING;
        """, (file_name, datetime.now()))

        # Fetch the file_id for the given file_name
        cursor.execute(
            "SELECT id FROM files WHERE file_name = %s;", (file_name,))
        row = cursor.fetchone()
        if row:
            file_id = row[0]
        else:
            raise ValueError(f"File '{file_name}' not found in database.")

        # Insert chunk into chunks table with page number
        cursor.execute("""
            INSERT INTO chunks (file_id, chunk_text, chunk_number, page, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (file_id, chunk_text, chunk_number, page, datetime.now()))

        chunk_id = cursor.fetchone()[0]

        # Insert embedding as an array if the column type is FLOAT8[]
        cursor.execute("""
            INSERT INTO embeddings (chunk_id, embedding, created_at)
            VALUES (%s, %s, %s);
        """, (chunk_id, embedding, datetime.now()))  # Insert embedding directly if it's now a list

        # Commit the transaction
        conn.commit()
        print(
            f"Chunk {chunk_number} embedding for file '{file_name}' (page {page}) successfully stored.")

    except (ValueError, psycopg2.Error) as e:
        conn.rollback()  # Rollback if any exception occurs
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def extract_text_from_pdf(file_path):
    """
    Extracts text from each page of a PDF file using pdfplumber.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of tuples (text, page_number) for each page in the PDF.
    """
    text_pages = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:  # Only add pages with text
                text_pages.append((text, page_number))
    return text_pages


def chunk_text_by_page(text_pages, chunk_size=1024):
    """
    Splits text from each page into chunks.

    Args:
        text_pages (list): A list of tuples with text and page numbers.
        chunk_size (int): The size of each chunk in characters.

    Returns:
        list: A list of tuples (chunk_text, page_number).
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
        print(chunk)
        embedding = embed_text(chunk)
        store_embedding_in_postgres(file_name, chunk, embedding, i, page)


def delete_file_from_postgres(file_name):
    """
    Deletes a file and its associated chunks and embeddings from the PostgreSQL database.

    Args:
        file_name (str): The name of the file to delete.
    """
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM files WHERE file_name = %s;", (file_name,))

        conn.commit()
        print(f"File '{file_name}' and associated data successfully deleted.")

    except Exception as e:
        print(f"Error deleting file: {e}")

    finally:
        cursor.close()
        conn.close()
