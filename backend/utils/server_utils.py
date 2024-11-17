from backend.utils.constants import serverConstants, postgreSQLConstants, legifrance_postgreSQLConstants
from backend.utils.pdf_utils import embed_text
from psycopg2.extras import RealDictCursor
import psycopg2
import requests
import json
import os
from dotenv import load_dotenv
import subprocess
import signal

# Constants

db_config = postgreSQLConstants.db_config
db_config_legifrance = legifrance_postgreSQLConstants.db_config

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

load_dotenv()


# Server launch functions

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


def launch_frontend_server():
    os.system("cd frontend && npm start")


def launch_backend_server():
    root_path = os.getcwd()
    subprocess.Popen(["uvicorn", "backend.main:app",
                     "--reload"], cwd=root_path)


# Server shutdown functions

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


# RAG model functions

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


def find_similar_chunks_legifrance(query_text, top_n=3):
    """
    Finds the top N most similar chunks to the query text.

    Args:
        query_text (str): The query for which similar chunks are searched.
        top_n (int): The number of similar chunks to retrieve. Default is 3.

    Returns:
        list: A list of dictionaries containing the top N similar chunks with their details.
    """
    query_embedding = embed_text(query_text)
    if not query_embedding:
        raise ValueError("Failed to generate embedding for the query text.")
    embedding_str = f"[{', '.join(map(str, query_embedding['embedding']))}]"

    with psycopg2.connect(**db_config_legifrance) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                sql_query = """
                    SELECT c.chunk_text, c.article_id, a.title, a.section, 
                           c.embedding <=> %s AS similarity
                    FROM chunks c
					JOIN articles a ON c.article_id = a.article_id
					WHERE embedding IS NOT NULL
                    
                    ORDER BY similarity ASC
					LIMIT %s;
                """
                cursor.execute(
                    sql_query, (embedding_str, top_n))
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(f"Error retrieving similar chunks: {e}")
                return []


def find_similar_chunks(query_text, top_n=3):
    """
    Finds the top N most similar chunks to the query text.

    Args:
        query_text (str): The query for which similar chunks are searched.
        top_n (int): The number of similar chunks to retrieve. Default is 3.

    Returns:
        list: A list of dictionaries containing the top N similar chunks with their details.
    """
    query_embedding = embed_text(query_text)
    if not query_embedding:
        raise ValueError("Failed to generate embedding for the query text.")
    embedding_str = f"[{', '.join(map(str, query_embedding['embedding']))}]"

    with psycopg2.connect(**db_config) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                sql_query = """
                    SELECT c.chunk_text, c.chunk_number, c.page, f.file_name, 
                           e.embedding <=> %s AS similarity
                    FROM embeddings e
                    JOIN chunks c ON e.chunk_id = c.id
                    JOIN files f ON c.file_id = f.id
                    ORDER BY similarity
                    LIMIT %s;
                """
                cursor.execute(
                    sql_query, (embedding_str, top_n))
                results = cursor.fetchall()
                return results
            except Exception as e:
                print(f"Error retrieving similar chunks: {e}")
                return []


def find_and_format_similar_chunks(query_text, top_n=3, similarity_threshold=0.7):
    """
    Finds the top N similar chunks to a query, filters by similarity, and formats them for language model input.

    Args:
        query_text (str): The query text for similarity search.
        top_n (int): The number of top similar chunks to retrieve. Default is 3.
        similarity_threshold (float): The maximum similarity score to include. Default is 0.7.

    Returns:
        str: A formatted string of the relevant chunks for language model input.
    """
    similar_chunks = find_similar_chunks(query_text, top_n=top_n)
    filtered_chunks = [
        chunk for chunk in similar_chunks if chunk["similarity"] <= similarity_threshold
    ]
    formatted_text = "\n\n".join(
        f"File: {chunk['file_name']}, Page: {chunk['page']}, Chunk: {chunk['chunk_number']}\n{chunk['chunk_text']}"
        for chunk in filtered_chunks
    )

    return formatted_text


def find_and_format_similar_chunks_legifrance(query_text, top_n=3, similarity_threshold=0.7):
    """
    Finds the top N similar chunks to a query, filters by similarity, and formats them for language model input.

    Args:
        query_text (str): The query text for similarity search.
        top_n (int): The number of top similar chunks to retrieve. Default is 3.
        similarity_threshold (float): The maximum similarity score to include. Default is 0.7.

    Returns:
        str: A formatted string of the relevant chunks for language model input.
    """
    similar_chunks = find_similar_chunks_legifrance(query_text, top_n=top_n)
    filtered_chunks = [
        chunk for chunk in similar_chunks if chunk["similarity"] <= similarity_threshold
    ]
    formatted_text = "\n\n".join(
        f"File: {chunk['section'] + chunk['title']} \n{chunk['chunk_text']}"
        for chunk in filtered_chunks
    )

    return formatted_text


def format_prompt(question, retrieved_chunks, language="fr"):
    """
    Formats the prompt for the model based on the presence of retrieved chunks.

    Args:
        question (str): The question to be answered by the model.
        retrieved_chunks (str): The retrieved chunks formatted for the language model, or an empty string if none are found.
        language (str): Language for the prompt template. Options are "en" (English) and "fr" (French).

    Returns:
        str: The formatted prompt for the model.
    """
    template_RAG_en = (
        "You are a knowledgeable assistant for a lawyer. Based on the following information: {knowledge}, "
        "please answer the following question with the highest accuracy and based strictly on the provided knowledge: {question}."
    )
    template_RAG_fr = (
        "Vous êtes un assistant juridique expérimenté pour un avocat. Sur la base des informations suivantes : {knowledge}, "
        "répondez à la question suivante avec la plus grande précision et en vous fondant strictement sur les connaissances fournies : {question}."
    )
    if language == "fr":
        template = template_RAG_fr
    else:
        template = template_RAG_en

    if retrieved_chunks:
        prompt = template.format(knowledge=retrieved_chunks, question=question)
    else:
        if language == "fr":
            prompt = f"Vous êtes un assistant juridique pour un avocat de renom. Répondez à la question suivante le plus précisément possible : {question}."
        else:
            prompt = f"You are a lawyer assistant. Answer the following question the most accurately you can: {question}."

    return prompt


def format_prompt_legifrance(question, retrieved_chunks, language="fr"):
    """
    Formats the prompt for the model based on the presence of retrieved chunks.

    Args:
        question (str): The question to be answered by the model.
        retrieved_chunks (str): The retrieved chunks formatted for the language model, or an empty string if none are found.
        language (str): Language for the prompt template. Options are "en" (English) and "fr" (French).

    Returns:
        str: The formatted prompt for the model.
    """
    template_RAG_en = (
        "You are a knowledgeable assistant for a lawyer. Based on the following information extracted from articles of the french law: {knowledge}, "
        "please answer the following question with the highest accuracy and based strictly on the provided knowledge: {question}."
    )
    template_RAG_fr = (
        "Vous êtes un assistant juridique expérimenté pour un avocat. Sur la base des extraits d'articles suivants : {knowledge}, "
        "répondez à la question suivante avec la plus grande précision et en vous fondant strictement sur les connaissances fournies : {question}."
    )
    if language == "fr":
        template = template_RAG_fr
    else:
        template = template_RAG_en

    if retrieved_chunks:
        prompt = template.format(knowledge=retrieved_chunks, question=question)
    else:
        if language == "fr":
            prompt = f"Vous êtes un assistant juridique pour un avocat de renom. Répondez à la question suivante le plus précisément possible : {question}."
        else:
            prompt = f"You are a lawyer assistant. Answer the following question the most accurately you can: {question}."

    return prompt

# Server request functions


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


def request_answer_with_retrieval(question, similarity_threshold=0.7, top_n=3):
    """
    Performs a similarity search for relevant chunks, formats a prompt, and sends a request to the server.

    Args:
        question (str): The question to be answered by the model.
        similarity_threshold (float): The maximum similarity score to include. Default is 0.7.
        top_n (int): The number of similar chunks to retrieve. Default is 3.

    Returns:
        str or generator: The server's response if non-streaming, or a generator for streaming.
    """
    retrieved_chunks = find_and_format_similar_chunks(
        question, top_n=top_n, similarity_threshold=similarity_threshold)
    prompt = format_prompt(question, retrieved_chunks)
    return request_answer(prompt)


def request_answer_with_retrieval_legifrance(question, similarity_threshold=0.7, top_n=8):
    """
    Performs a similarity search for relevant chunks, formats a prompt, and sends a request to the server.

    Args:
        question (str): The question to be answered by the model.
        similarity_threshold (float): The maximum similarity score to include. Default is 0.7.
        top_n (int): The number of similar chunks to retrieve. Default is 3.

    Returns:
        str or generator: The server's response if non-streaming, or a generator for streaming.
    """
    retrieved_chunks = find_and_format_similar_chunks_legifrance(
        question, top_n=top_n, similarity_threshold=similarity_threshold)
    prompt = format_prompt_legifrance(
        question, retrieved_chunks, language="fr")
    return request_answer(prompt)
