from fastapi import HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from backend.utils.db_helpers import delete_file_from_postgres
from backend.utils.pdf_utils import chunk_and_embed_file_and_store
from pathlib import Path
import os
import shutil

TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


# Functions to handle file uploads, deletions, and listing

async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunk_size = 1024
        chunk_and_embed_file_and_store(file_path, chunk_size)
        response = {
            "message": "File uploaded and processed successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {e}")
    return response


async def delete_file(file_name: str):
    deleted = False
    for root, dirs, files in os.walk(TEMP_DIR):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
            deleted = True
            break
    delete_file_from_postgres(file_name)
    if deleted:
        return {"message": f"File '{file_name}' deleted successfully"}
    else:
        raise HTTPException(
            status_code=404, detail=f"File '{file_name}' not found")


async def list_files():
    files = []
    for file_name in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            extension = Path(file_name).suffix
            files.append({"name": file_name, "url": f"/uploads/{file_name}",
                         "type": extension.replace(".", "")})
    return JSONResponse(content={"files": files})
