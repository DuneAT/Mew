import requests
import json
from backend.utils.constants import serverConstants


def embed_text(text):
    """
    Embeds text using the Ollama server.
    """
    response = requests.post(
        serverConstants.url_embedding, json={"text": text})
    return json.loads(response.text).get("embedding", [])
