class ModelFileConstants:
    modelfile_template = """<|im_start|>system {{ .System }}<|im_end|><|im_start|>user {{ .Prompt }}<|im_end|><|im_start|>assistant<|im_end|>"""
    num_ctx = 8000

class serverConstants:
    url_serve = "http://localhost:11434//api/generate"
    model_path = "models/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"