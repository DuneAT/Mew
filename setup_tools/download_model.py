from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import os
import dotenv

#dotenv import and login

dotenv.load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(hf_token)

#model download

model_name = "meta-llama/Meta-Llama-3.1-8B"

tokenizer = AutoTokenizer.from_pretrained(model_name,cache_dir="models/")
