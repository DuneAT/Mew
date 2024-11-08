import os
from pathlib import Path
import shutil
from backend.utils.constants import serverConstants
from backend.utils.db_helpers import store_embedding_in_postgres, delete_file_from_postgres
from backend.utils.pdf_utils import extract_text_from_pdf, chunk_text_by_page
from backend.utils.embedding_utils import embed_text

TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


async def save_uploaded_file(file):
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunk_size = 1024
    chunk_and_embed_file_and_store(file_path, chunk_size)
    return {"message": "File uploaded and processed successfully", "file_path": file_path}


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


def delete_file_and_cleanup(file_name: str):
    deleted = False
    for root, dirs, files in os.walk(TEMP_DIR):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
            deleted = True
            break
    delete_file_from_postgres(file_name)
    if not deleted:
        raise FileNotFoundError
    return {"message": f"File '{file_name}' deleted successfully"}


def list_all_files():
    files = []
    for file_name in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            extension = Path(file_name).suffix
            files.append({"name": file_name, "url": f"/uploads/{file_name}",
                         "type": extension.replace(".", "")})
    return files


def shutdown_event():
    shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
