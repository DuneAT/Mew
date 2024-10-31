import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import subprocess
import signal
from utils.constants import serverConstants

load_dotenv()

url = serverConstants.url_serve
model_path = serverConstants.model_path
model_path = "models/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
modelfile_path = "modelfiles/ModelFile_" + Path(model_path).stem + ".txt"
mew_model = "mew_model"
port = 11434  # change with the port you are using, by default it is 11434 for ollama


def create_model_file(modelfile_text):
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


def launch_ollama_server(modelfile_path=modelfile_path):
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
    print(modelfile_path)
    os.system(f"ollama create {mew_model} -f {modelfile_path}")
    print(f"Server launched successfully on port {port}.")


def request_answer(prompt, mew_model="mew_model"):
    """
    Sends a request to a server with a given prompt and model, and returns the server's response.

    Args:
        prompt (str): The prompt to send to the server.
        mew_model (str, optional): The model to use for the request. Defaults to "mew_model".

    Returns:
        str: The server's response if the request is successful, otherwise "Server Error".
    """
    headers = {"Content-Type": "application/json"}

    data = {
        "model": mew_model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
        return "Server Error"


def request_answer_stream(prompt):
    """
    Sends a request to the server with the given prompt and returns the response.

    Args:
        prompt (str): The prompt to send to the server.

    Returns:
        str: The server's response if the request is successful, otherwise "Server Error".
    """
    headers = {"Content-Type": "application/json"}

    data = {
        "model": mew_model,
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
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
