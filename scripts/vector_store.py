"""
============================================================
Ordinex AI Compliance System
Vector Store Builder (ChromaDB)
============================================================

Purpose:
    Loads regulation embeddings and stores them inside
    a persistent ChromaDB vector database.

Author: Ordinex Team
============================================================
"""

import json
import os
import numpy as np
import chromadb
from chromadb.config import Settings

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMBEDDINGS_PATH = os.path.join(
    BASE_DIR,
    "Data",
    "Embeddings",
    "embeddings.npy"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "Data",
    "Embeddings",
    "metadata.json"
)

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "vector_db"
)

# ---------------------------------------------------------
# Load Files
# ---------------------------------------------------------

print("=" * 60)
print("Loading embeddings...")

embeddings = np.load(EMBEDDINGS_PATH)

print("Loading metadata...")

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)

print(f"Loaded {len(metadata)} regulations.")

# ---------------------------------------------------------
# Create ChromaDB Client
# ---------------------------------------------------------

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

# Delete old collection if it exists
try:
    client.delete_collection("ordinex_regulations")
except:
    pass

collection = client.create_collection(
    name="ordinex_regulations"
)

print("ChromaDB collection created.")

# ---------------------------------------------------------
# Insert Data
# ---------------------------------------------------------

print("Storing vectors...")

ids = []
documents = []
metadatas = []

for item in metadata:

    ids.append(item["id"])

    documents.append(item["text"])

    metadatas.append({
        "country": item["country"],
        "law": item["law"],
        "category": item["category"],
        "risk": item["risk"]
    })

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print()
print("=" * 60)
print("Vector Database Created Successfully!")
print(f"Total Regulations : {collection.count()}")
print(f"Database Location : {VECTOR_DB_PATH}")
print("=" * 60)