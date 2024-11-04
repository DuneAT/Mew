from utils.useful_strings import UsefulStrings
from utils.constants import ModelFileConstants, serverConstants
from server_utils import create_model_file, launch_ollama_server

# constants

url = serverConstants.url_serve
model_path = serverConstants.model_path
model_path = "models/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"


num_ctx = ModelFileConstants.num_ctx
modelfile_template = ModelFileConstants.modelfile_template
modelfile_text = UsefulStrings.modelfile_text.format(
    model_path=model_path, num_ctx=num_ctx, modelfile_template=modelfile_template)


# create model file and launch server

create_model_file(modelfile_text)
launch_ollama_server()
