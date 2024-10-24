from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

login(token = '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')

tokenizer = AutoTokenizer.from_pretrained(
"meta-llama/Meta-Llama-3.1-8B",
cache_dir="models/",
)

model = AutoModelForCausalLM.from_pretrained(
"meta-llama/Meta-Llama-3.1-8B",
cache_dir="models/",
device_map="auto",
)