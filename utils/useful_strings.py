class UsefulStrings :

    modelfile_text = """FROM {model_path}

    PARAMETER num_ctx {num_ctx}

    TEMPLATE {modelfile_template}

    PARAMETER stop <|im_end|>
    PARAMETER stop <|im_start|>user
    PARAMETER stop <|end|>"""
    
    
    