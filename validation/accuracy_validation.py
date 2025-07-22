import pandas as pd

# Carica il file Excel
df = pd.read_excel("inferences/risultati_validazione_gemma_test300.xlsx")

# Rimuove righe con valori mancanti
df = df.dropna(subset=['input_file_image_name', 'matched_file_image_name'])

# Estrai la parte prima di "_diff" e aggiungi ".jpg"
df['input_base'] = df['input_file_image_name'].apply(lambda x: x.split('_diff')[0] + '.jpg')

# Verifica corrispondenza
df['match'] = df['input_base'] == df['matched_file_image_name']

# Calcola accuracy
accuracy = df['match'].mean()
print(f"Accuracy: {accuracy:.2%}")

# Filtra mismatch
mismatch_df = df[df['match'] == False]

# Salva in un nuovo file Excel
mismatch_df.to_excel("mismatch_risultati_gemma_test300.xlsx", index=False)

# Filtra mismatch
match_df = df[df['match'] != False]

# Salva in un nuovo file Excel
match_df.to_excel("match_risultati_gemma_test300.xlsx", index=False)
