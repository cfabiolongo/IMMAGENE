# pip install pandas sentence-transformers faiss-cpu tqdm

import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Inizializza tqdm per pandas
tqdm.pandas()

# Inizializza modello
model = SentenceTransformer('all-MiniLM-L6-v2')

# Carica Excel
df = pd.read_excel('inferences/image_descriptions_t08_34b.xlsx')

# Calcola embedding con barra di progresso
df['embedding'] = df['description'].progress_apply(
    lambda d: model.encode(d).astype(np.float32).tobytes()
)

# Crea DB SQLite
conn = sqlite3.connect('inferences/image_descriptions_t08_34b.db')
c = conn.cursor()

# Crea tabella
c.execute('''
CREATE TABLE IF NOT EXISTS immagini (
    id INTEGER PRIMARY KEY,
    file_image_name TEXT,
    description TEXT,
    embedding BLOB
)
''')

# Inserisce righe con barra di progresso
for _, row in tqdm(df.iterrows(), total=len(df), desc="Inserimento nel DB"):
    c.execute('''
        INSERT INTO immagini (file_image_name, description, embedding)
        VALUES (?, ?, ?)
    ''', (row['file_image_name'], row['description'], row['embedding']))

conn.commit()
conn.close()
print("✅ Database creato con successo.")
