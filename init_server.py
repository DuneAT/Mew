import os
from utils.useful_strings import UsefulStrings
from utils.constants import ModelFileConstants, serverConstants
from utils.server_utils import create_model_file, launch_ollama_server

url = serverConstants.url_serve
model_path = serverConstants.model_path


num_ctx = ModelFileConstants.num_ctx
modelfile_template = ModelFileConstants.modelfile_template
modelfile_text = UsefulStrings.modelfile_text.format(
    model_path=model_path, num_ctx=num_ctx, modelfile_template=modelfile_template)

# if url already in use, shut

os.system("kill -9 $(lsof -i:11434)")

create_model_file(modelfile_text)
launch_ollama_server()
