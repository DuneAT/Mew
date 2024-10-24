import requests 
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("url_serve")
model_path = os.getenv("model_path")


def launch_ollama_server():
    


def request_answer(prompt):
    headers = {"Content-Type" : "application/json"}

    data = {
        "model" : model_path,
        "prompt" : prompt,
        "stream" : False
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
    headers = {"Content-Type" : "application/json"}

    data = {
        "model" : model_path,
        "prompt" : prompt,
        "stream" : True
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        return actual_response
    else:
        return "Erreur de serveur"