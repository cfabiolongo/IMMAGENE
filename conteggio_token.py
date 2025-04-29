from transformers import CLIPTokenizer

# Carica il tokenizer di CLIP
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")

# Esempio: prompt da controllare
prompt = "The image shows a bus on a road, with trees and buildings in the background. The bus appears to be either red or maroon with white windows and doors. It has a destination sign at its front but the text is not fully visible. There are other buses and cars around it, indicating that this might be a busy city street."

# Conta i token
num_tokens = len(tokenizer(prompt)["input_ids"])

print(f"Numero di token nel prompt: {num_tokens}")
