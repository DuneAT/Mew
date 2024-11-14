from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
from backend.controllers.file_controllers import list_files, upload_file, delete_file

router = APIRouter()


@router.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    return await upload_file(file)


@router.delete("/api/delete-file")
async def delete(file_name: str):
    return await delete_file(file_name)


@router.get("/api/list-files")
async def list():
    return await list_files()


@router.on_event("shutdown")
def shutdown_event():
    shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
