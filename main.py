from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

if torch.cuda.is_available():
    torch.set_default_device("cuda")
    torch.set_default_dtype(torch.float16)
# Path to the local model
model_path = "models/llama3"
torch.cuda.empty_cache()

# Load the tokenizer and model from the local directory
#tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# # Input text for generating continuation
# input_text = "Once upon a time"

# # Tokenize the input
# inputs = tokenizer(input_text, return_tensors="pt")

# # Generate text
# with torch.no_grad():
#     output_sequences = model.generate(
#         **inputs,
#         max_length=50,  # Set the max length of the generated text
#         num_return_sequences=1,  # Set how many sequences you want to generate
#     )

# # Decode the generated sequences back into text
# generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)

# print(f"Generated text: {generated_text}")
