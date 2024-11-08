import requests
import json
import os
from dotenv import load_dotenv
import subprocess
import signal
from utils.constants import serverConstants

load_dotenv()

stream = serverConstants.stream

port = serverConstants.port

url_generate = serverConstants.url_generate
url_embedding = serverConstants.url_embedding

mew_model = serverConstants.mew_model
model_path = serverConstants.model_path
modelfile_path = serverConstants.modelfile_path

embedding_model = serverConstants.embedding_model
embedding_path = serverConstants.embedding_path
modelfile_embedding_path = serverConstants.modelfile_embedding_path


def create_model_file(modelfile_text, modelfile_path):
    """
    Creates a model file with the given text.

    Args:
        modelfile_text (str): The text content to be written to the model file.

    Raises:
        IOError: If the file cannot be written.
    """
    with open(modelfile_path, 'w') as file:
        file.write(modelfile_text)
    print(f"{modelfile_path} created successfully!")


def launch_ollama_server():
    """
    Launches the Ollama server with the specified model file.

    Args:
        modelfile_path (str): The path to the model file to be used by the server.

    Returns:
        None

    Side Effects:
        Executes a system command to create the Ollama server with the specified model file.
        Prints a success message indicating the server has been launched and the port it is running on.
    """
    os.system(f"ollama create {mew_model} -f {modelfile_path}")
    os.system(f"ollama create {embedding_model} -f {modelfile_embedding_path}")
    print(f"Server launched successfully on port {port}.")


def request_answer_not_stream(prompt):
    """
    Sends a request to the server with the given prompt and model, and returns the server's response.

    Args:
        prompt (str): The prompt to send to the server.
        mew_model (str): The model to use for generating the response. Defaults to the value of `mew_model`.

    Returns:
        str: The server's response if the request is successful, otherwise "Server Error".

    Raises:
        Exception: If there is an error during the request, it prints the error message and returns "Server Error".
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": mew_model,  # Replace with your actual model name
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            url_generate, headers=headers, data=json.dumps(data))
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


def request_answer_stream(prompt):
    """
    Sends a request to the server with the given prompt and returns the response in a stream.

    Args:
        prompt (str): The prompt to send to the server.

    Yields:
        str: Each chunk of the server's response as it arrives.
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
                        data = json.loads(chunk)
                        actual_response = data.get("response", "")
                        yield actual_response
            else:
                yield "Server Error"
    except requests.RequestException as e:
        yield f"Request Error: {str(e)}"


def request_answer(prompt):
    """
    Sends a request to the server with the given prompt and returns the response.

    Args:
        prompt (str): The prompt to send to the server.
        stream (bool): Whether to use streaming mode for the response. Default is False.

    Returns:
        str: The server's response if the request is successful, otherwise "Server Error".
    """
    if stream:
        response = request_answer_stream(prompt)
        return response
    else:
        response = request_answer_not_stream(prompt)
        return response


def request_embedding(text):
    """
    Sends a request to the server with the given text and returns the corresponding embedding.

    Args:
        text (str): The text to send to the server.

    Returns:
        str: The server's response if the request is successful, otherwise "Server Error".
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
            embedding_vector = response.json().get("embedding")
            return embedding_vector
        else:
            return "Server Error"
    except Exception as e:
        print(f"Error during request: {e}")
        return "Server Error"


def find_pid_by_port(port=11434):
    """
    Find the process ID (PID) of the process that is using the specified port.

    Args:
        port (int): The port number to check. Default is 11434.

    Returns:
        int: The PID of the process using the specified port, or None if no process is found.

    Raises:
        subprocess.CalledProcessError: If the subprocess call fails.
    """
    try:
        result = subprocess.check_output(f"lsof -i :{port} -t", shell=True)
        pid = int(result.strip())
        return pid
    except subprocess.CalledProcessError:
        return None


def kill_process(pid):
    """
    Terminates a process with the given process ID (PID).

    Args:
        pid (int): The process ID of the process to be terminated.

    Raises:
        OSError: If an error occurs while attempting to terminate the process.

    Example:
        kill_process(1234)
    """
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process {pid} terminated successfully.")
    except OSError as e:
        print(f"Error terminating process {pid}: {e}")


def launch_backend_server():
    """
    Launches the backend server.

    Returns:
        None

    Side Effects:
        Executes a system command to launch the backend server.
        Prints a success message indicating the server has been launched.
    """
    os.system("uvicorn main:app --reload")
    print("Backend server launched successfully.")
