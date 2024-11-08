import json
import requests
from backend.utils.constants import serverConstants
from backend.utils.server_management import launch_ollama_server, find_pid_by_port, kill_process

stream = serverConstants.stream
port = serverConstants.port

mew_model = serverConstants.mew_model
url_generate = serverConstants.url_generate
url_embedding = serverConstants.url_embedding
embedding_model = serverConstants.embedding_model


def request_answer(prompt, use_stream=stream):
    """
    Sends a request to the server with the given prompt and returns the response.
    """
    if use_stream:
        return request_answer_stream(prompt)
    else:
        return request_answer_not_stream(prompt)


def request_answer_not_stream(prompt):
    """
    Sends a non-streaming request to the server with the given prompt and returns the response.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": mew_model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            url_generate, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return "Server Error"
    except Exception as e:
        print(f"Error during request: {e}")
        return "Server Error"


def request_answer_stream(prompt):
    """
    Sends a streaming request to the server with the given prompt and returns each response chunk.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": mew_model,
        "prompt": prompt,
        "stream": True
    }
    try:
        with requests.post(url_generate, headers=headers, data=json.dumps(data), stream=True) as response:
            if response.status_code == 200:
                for chunk in response.iter_lines(decode_unicode=True):
                    if chunk:
                        yield json.loads(chunk).get("response", "")
            else:
                yield "Server Error"
    except requests.RequestException as e:
        yield f"Request Error: {str(e)}"


def request_embedding(text):
    """
    Sends a request to the server with the given text and returns the corresponding embedding.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": embedding_model,
        "prompt": text
    }
    try:
        response = requests.post(
            url_embedding, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get("embedding", [])
        else:
            return "Server Error"
    except Exception as e:
        print(f"Error during request: {e}")
        return "Server Error"
