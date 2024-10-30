from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from utils.constants import serverConstants

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's development server
    allow_methods=["*"],
    allow_headers=["*"],
)

def request_answer(prompt):
    """
    Sends a request to the LLM server with the given prompt and retrieves the response.
    Args:
        prompt (str): The input prompt to be sent to the LLM server.
    Returns:
        str: The response from the LLM server if the request is successful.
             Returns "Server Error" if there is an error during the request or if the server responds with an error status code.
    Raises:
        Exception: If there is an error during the request, it will be caught and printed.
    """
    url = serverConstants.url_serve  # Replace with the actual LLM server URL
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "mew_model", 
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


@app.post("/api/ask")
async def ask(request: Request):
    """
    Handle an incoming request to generate a response based on a given prompt.

    Args:
        request (Request): The incoming HTTP request containing JSON data.

    Returns:
        dict: A dictionary containing the generated response.
    """
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}
