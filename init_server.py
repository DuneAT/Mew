import os
from utils.useful_strings import UsefulStrings
from utils.constants import ModelFileConstants, serverConstants
from utils.server_utils import create_model_file

url = serverConstants.url_serve
model_path = serverConstants.model_path


num_ctx = ModelFileConstants.num_ctx
modelfile_template = ModelFileConstants.modelfile_template
modelfile_text = UsefulStrings.modelfile_text(model_path, num_ctx, modelfile_template)

create_model_file(modelfile_text)
