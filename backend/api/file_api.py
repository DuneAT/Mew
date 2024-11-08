from fastapi import APIRouter
from backend.controllers.file_controllers import upload_file, delete_file, list_files

router = APIRouter()

router.post("/upload")(upload_file)
router.delete("/delete-file")(delete_file)
router.get("/list-files")(list_files)
