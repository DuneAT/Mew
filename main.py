from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import os
import shutil
from datetime import datetime

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

# Your LLM function
def request_answer(prompt):
    url = "http://localhost:11434/api/generate"  # Replace with the actual LLM server URL
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "mew_model",  # Replace with your actual model name
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            return actual_response
        else:
            return "Server Error"
    except Exception as e:
        print(f"Error during request: {e}")
        return "Server Error"

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
    # Create a unique session folder
    session_folder = os.path.join(TEMP_DIR, f"session-{datetime.now().timestamp()}")
    os.makedirs(session_folder, exist_ok=True)

    file_path = os.path.join(session_folder, file.filename)

    # Save the file to the session folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Response to the client
    response = {"message": "File uploaded successfully", "file_path": file_path}

    # Optional: Schedule the folder to be deleted after the session
    # shutil.rmtree(session_folder) # Uncomment this line for immediate cleanup after the response

    return response
