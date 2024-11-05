from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import requests

app = FastAPI()

# CORS middleware to allow React frontend to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's development server
    allow_methods=["*"],
    allow_headers=["*"],
)

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
