import requests 
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("url_serve")
model_path = os.getenv("model_path")

headers = {"Content-Type" : "application/json"}

data = {
    "model" : "modele1",
    "prompt" : "why is the sky blue ?",
    "stream" : False
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    response_text = response.text
    data = json.loads(response_text)
    actual_response = data["response"]
    print(actual_response)
else:
    print("error")