from utils.useful_strings import UsefulStrings
from utils.constants import ModelFileConstants, serverConstants
from utils.server_utils import create_model_file, launch_ollama_server, launch_backend_server

# constants

model_path = serverConstants.model_path
modelfile_path = serverConstants.modelfile_path

modelfile_embedding_path = serverConstants.modelfile_embedding_path
embedding_path = serverConstants.embedding_path

num_ctx = ModelFileConstants.num_ctx
modelfile_template = ModelFileConstants.modelfile_template
modelfile_text = UsefulStrings.modelfile_text.format(
    model_path=model_path, num_ctx=num_ctx, modelfile_template=modelfile_template)

modelfile_embedding_text = UsefulStrings.modelfile_embedding_text.format(
    model_path=embedding_path)


# create model file and launch server

create_model_file(modelfile_text, modelfile_path)
create_model_file(modelfile_embedding_text, modelfile_embedding_path)
launch_ollama_server()
launch_backend_server()
