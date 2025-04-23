# pip install pandas sentence-transformers faiss-cpu

import pandas as pd
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# Inizializza modello
model = SentenceTransformer('all-MiniLM-L6-v2')

# Carica Excel
df = pd.read_excel('image_descriptions.xlsx')  # ← Cambia con il tuo file

# Calcola embedding
df['embedding'] = df['description'].apply(lambda d: model.encode(d).astype(np.float32).tobytes())

# Crea DB SQLite
conn = sqlite3.connect('descrizioni.db')
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

# Inserisce righe
for _, row in df.iterrows():
    c.execute('''
        INSERT INTO immagini (file_image_name, description, embedding)
        VALUES (?, ?, ?)
    ''', (row['file_image_name'], row['description'], row['embedding']))

conn.commit()
conn.close()
print("✅ Database creato con successo.")
