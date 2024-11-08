from fastapi import HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from backend.services.file_services import save_uploaded_file, delete_file_and_cleanup, list_all_files


async def upload_file(file: UploadFile = File(...)):
    try:
        response = await save_uploaded_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing file: {e}")
    return response


async def delete_file(file_name: str):
    try:
        response = delete_file_and_cleanup(file_name)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"File '{file_name}' not found")
    return response


async def list_files():
    return JSONResponse(content={"files": list_all_files()})
