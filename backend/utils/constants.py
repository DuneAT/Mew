import os
from dotenv import load_dotenv

load_dotenv()


class ModelFileConstants:
    modelfile_template = """<|im_start|>system {{ .System }}<|im_end|><|im_start|>user {{ .Prompt }}<|im_end|><|im_start|>assistant<|im_end|>"""
    num_ctx = 8000


class serverConstants:
    port = 11434  # need to be changed according to following urls

    url_generate = "http://localhost:11434//api/generate"
    url_embedding = "http://localhost:11434/api/embeddings"

    model_path = "backend/models/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
    embedding_path = "backend/models/mxbai-embed-large-v1-f16.gguf"

    modelfile_path = "Modelfile"
    modelfile_embedding_path = "ModelFileEmb"

    mew_model = "mew_model"
    embedding_model = "embedding_model"

    stream = False


class postgreSQLConstants:
    dbname = 'embedding_db'
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = 'localhost'
    port = 5433
    db_config = {
        'dbname': dbname,
        'user': user,
        'password': password,
        'host': host,
        'port': port
    }
