from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils.server_utils import request_answer
from fastapi.staticfiles import StaticFiles
import os
import shutil
from pathlib import Path

app = FastAPI()

# CORS middleware to allow React frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's development server
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a temporary directory for storing files
TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# API endpoint to handle requests from the frontend
@app.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}

# API endpoint for file upload
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(TEMP_DIR, file.filename)

    # Save the file to the TEMP_DIR directly
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    response = {"message": "File uploaded successfully", "file_path": file_path}
    return response

# New API endpoint to delete a specific file
@app.delete("/api/delete-file")
async def delete_file(file_name: str):
    # Search for the file in the TEMP_DIR
    deleted = False
    for root, dirs, files in os.walk(TEMP_DIR):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
            deleted = True
            break

    if deleted:
        return {"message": f"File '{file_name}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    
# Serve files in TEMP_DIR under the /uploads path
app.mount("/uploads", StaticFiles(directory=TEMP_DIR), name="uploads")

@app.get("/api/list-files")
async def list_files():
    files = []
    for file_name in os.listdir(TEMP_DIR):
        file_path = os.path.join(TEMP_DIR, file_name)
        if os.path.isfile(file_path):
            # Return the URL instead of the local file path
            extension = Path(file_name).suffix
            files.append({"name": file_name, "url": f"/uploads/{file_name}", "type": extension.replace(".", "")})
    return JSONResponse(content={"files": files})

@app.on_event("shutdown")
def shutdown_event():
    # Delete all files in TEMP_DIR when the application stops
    shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)  # Recreate the empty directory for the next run
