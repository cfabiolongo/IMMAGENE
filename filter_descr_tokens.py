import pandas as pd
from transformers import CLIPTokenizer

# Carica il tokenizer di CLIP
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-large-patch14")

# Percorsi dei file
input_excel_path = "image_descriptions_t08_34b_brief.xlsx"     # Sostituisci con il tuo file Excel di input
output_excel_path = "output_filtered.xlsx"

# Carica il file Excel
df = pd.read_excel(input_excel_path)

# Filtra le righe in base alla lunghezza dei token della description
def is_within_token_limit(text, max_tokens=77):
    return len(tokenizer(text)["input_ids"]) <= max_tokens

# Applica il filtro
filtered_df = df[df["description"].apply(is_within_token_limit)]

# Salva il nuovo file Excel
filtered_df.to_excel(output_excel_path, index=False)

print(f"File salvato: {output_excel_path} con {len(filtered_df)} righe.")
