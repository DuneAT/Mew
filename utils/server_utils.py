import requests
import json
import os
from dotenv import load_dotenv
from utils.constants import serverConstants

load_dotenv()

url = serverConstants.url_serve
model_path = serverConstants.model_path


def create_model_file(modelfile_text):
    filename = "ModelFile_" + model_path.split("/")[-1] + ".txt"
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write(modelfile_text)
        print(f"{filename} created successfully!")
    else:
        print(f"{filename} already exists.")


def launch_ollama_server(mew_model="mew_model"):
    modelfile = "ModelFile_" + model_path.split("/")[-2] + ".txt"
    os.system(f"ollama create {mew_model} -f {modelfile}")


def request_answer(prompt):
    headers = {"Content-Type": "application/json"}

    data = {
        "model": model_path,
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
        return "Erreur de serveur"


def request_answer_stream(prompt):
    headers = {"Content-Type": "application/json"}

    data = {
        "model": model_path,
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
        return "Erreur de serveur"
