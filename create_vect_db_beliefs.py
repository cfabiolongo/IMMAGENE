# pip install pandas sentence-transformers faiss-cpu tqdm

import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Inizializza tqdm per pandas
tqdm.pandas()

print("loading model...")
# Inizializza modello
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"model {model} loaded.")

# Carica Excel
df = pd.read_excel('inferences/image_descriptions_t08_34b_brief.xlsx')

# Calcola embedding con barra di progresso
df['embedding'] = df['description'].progress_apply(
    lambda d: model.encode(d).astype(np.float32).tobytes()
)

# Crea DB SQLite
conn = sqlite3.connect('inferences/image_descriptions_t08_34b_brief.db')
c = conn.cursor()

# Crea tabella
c.execute('''
CREATE TABLE IF NOT EXISTS immagini (
    id INTEGER PRIMARY KEY,
    file_image_name TEXT,   
    description TEXT,
    beliefs TEXT,
    goals TEXT,
    actions TEXT,
    embedding BLOB
)
''')

# Inserisce righe con barra di progresso
for _, row in tqdm(df.iterrows(), total=len(df), desc="Inserimento nel DB"):
    c.execute('''
        INSERT INTO immagini (file_image_name, description, beliefs, goals, actions, embedding)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['file_image_name'], row['description'], row['beliefs'], row['goals'], row['actions'], row['embedding']))

conn.commit()
conn.close()
print("✅ Database creato con successo.")
