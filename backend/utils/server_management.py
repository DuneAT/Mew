import os
import subprocess
import signal
from backend.utils.constants import serverConstants

port = serverConstants.port
mew_model = serverConstants.mew_model
embedding_model = serverConstants.embedding_model
modelfile_path = serverConstants.modelfile_path
modelfile_embedding_path = serverConstants.modelfile_embedding_path


def create_model_file(modelfile_text, modelfile_path):
    """
    Creates a model file with the given text.
    """
    with open(modelfile_path, 'w') as file:
        file.write(modelfile_text)
    print(f"{modelfile_path} created successfully!")


def launch_ollama_server():
    """
    Launches the Ollama server with the specified model file.
    """
    os.system(f"ollama create {mew_model} -f {modelfile_path}")
    os.system(f"ollama create {embedding_model} -f {modelfile_embedding_path}")
    print(f"Server launched successfully on port {port}.")


def find_pid_by_port(port=port):
    """
    Finds the PID of the process that is using the specified port.
    """
    try:
        result = subprocess.check_output(f"lsof -i :{port} -t", shell=True)
        return int(result.strip())
    except subprocess.CalledProcessError:
        return None


def kill_process(pid):
    """
    Terminates a process with the given PID.
    """
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Process {pid} terminated successfully.")
    except OSError as e:
        print(f"Error terminating process {pid}: {e}")


def launch_frontend_server():
    os.system("cd frontend && npm start")


def launch_backend_server():
    root_path = os.getcwd()
    subprocess.Popen(["uvicorn", "backend.main:app",
                     "--reload"], cwd=root_path)
