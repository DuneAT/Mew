modelfile_template = """<|im_start|>system {{ .System }}<|im_end|><|im_start|>user {{ .Prompt }}<|im_end|><|im_start|>assistant<|im_end|>"""
num_ctx = 8000

class UsefulStrings :

    modelfile_text = """FROM {model_path}

    PARAMETER num_ctx {num_ctx}

    TEMPLATE {modelfile_template}

    PARAMETER stop <|im_end|>
    PARAMETER stop <|im_start|>user
    PARAMETER stop <|end|>"""
    
    
    