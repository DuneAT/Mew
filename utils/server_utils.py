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
modelfile_path = "modelfiles/ModelFile_" + Path(model_path).stem + ".txt"
mew_model = "mew_model"
port = 11434  # change with the port you are using, by default it is 11434 for ollama


def create_model_file(modelfile_text):
    with open(modelfile_path, 'w') as file:
        file.write(modelfile_text)
    print(f"{modelfile_path} created successfully!")


def launch_ollama_server(modelfile_path=modelfile_path):
    os.system(f"ollama create {mew_model} -f {modelfile_path}")
    print(f"Server launched successfully on port {port}.")


def request_answer(prompt, mew_model="mew_model"):
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
    try:
        result = subprocess.check_output(f"lsof -i :{port} -t", shell=True)
        pid = int(result.strip())
        return pid
    except subprocess.CalledProcessError:
        return None


def kill_process(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process {pid} terminated successfully.")
    except OSError as e:
        print(f"Error terminating process {pid}: {e}")
