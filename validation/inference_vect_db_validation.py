import sqlite3
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Inizializza modello
model = SentenceTransformer('all-MiniLM-L6-v2')


def find_most_similar(input_text):
    input_embedding = model.encode(input_text).astype(np.float32)

    conn = sqlite3.connect('inferences/image_descriptions_t08_34b_brief.db')
    c = conn.cursor()
    c.execute('SELECT id, file_image_name, description, embedding FROM immagini')
    rows = c.fetchall()
    conn.close()

    best_score = -1
    best_row = None

    for row in rows:
        row_id, file_name, desc, emb_blob = row
        emb_array = np.frombuffer(emb_blob, dtype=np.float32)
        score = cosine_similarity([input_embedding], [emb_array])[0][0]
        if score > best_score:
            best_score = score
            best_row = {
                "id": row_id,
                "file_image_name": file_name,
                "description": desc,
                "similarity": round(score, 4)
            }

    return best_row


# Applica la funzione su tutte le descrizioni di un file Excel
def process_excel_descriptions(file_path):
    df = pd.read_excel(file_path)

    # for gemma
    df['description'] = df['description'].str.replace('</start_of_turn>', '')
    df['description'] = df['description'].str.replace('</end_of_turn>', '')

    risultati = []
    for idx, row in df.iterrows():
        input_desc = row['description']
        file_name = row['file_image_name']
        print(f"\n📝 Elaborando '{file_name}'...")
        similar = find_most_similar(input_desc)
        risultati.append({
            "input_file_image_name": file_name,
            "input_description": input_desc,
            "matched_file_image_name": similar["file_image_name"],
            "matched_description": similar["description"],
            "similarity": similar["similarity"]
        })

    risultati_df = pd.DataFrame(risultati)
    return risultati_df


if __name__ == "__main__":
    excel_file = "inferences/image_descriptions_gemma_dipa-like.xlsx"
    df_risultati = process_excel_descriptions(excel_file)
    print("\n✅ Risultati completi:")
    # Salva i risultati in un nuovo file Excel
    output_file = "risultati_validazione_gemma_test300.xlsx"
    df_risultati.to_excel(output_file, index=False)
