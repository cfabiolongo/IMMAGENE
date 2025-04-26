import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Inizializza modello
model = SentenceTransformer('all-MiniLM-L6-v2')

def find_most_similar(input_text):
    input_embedding = model.encode(input_text).astype(np.float32)

    conn = sqlite3.connect('inferences/image_descriptions_t08_34b_plus_actions_70b.db')
    c = conn.cursor()
    c.execute('SELECT id, file_image_name, description, beliefs, goals, actions, embedding FROM immagini')
    rows = c.fetchall()
    conn.close()

    best_score = -1
    best_row = None

    for row in rows:
        row_id, file_name, desc, beliefs, goals, actions, emb_blob = row
        emb_array = np.frombuffer(emb_blob, dtype=np.float32)
        score = cosine_similarity([input_embedding], [emb_array])[0][0]
        if score > best_score:
            best_score = score
            best_row = {
                "id": row_id,
                "file_image_name": file_name,
                "description": desc,
                "belief": beliefs,
                "goals": goals,
                "actions": actions,
                "similarity": round(score, 4)
            }

    return best_row

# Esempio di utilizzo
if __name__ == "__main__":
    testo_input = input("Inserisci un testo per l'inferenza: ")
    risultato = find_most_similar(testo_input)
    print("\n🔍 Risultato più simile:")
    print(risultato)
