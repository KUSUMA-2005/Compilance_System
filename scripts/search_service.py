"""
============================================================
Ordinex AI Compliance System
Search Service
============================================================

Purpose:
Reusable semantic search service.

This module is used by:
    - Compliance Engine
    - Backend API
    - Future Chatbot
    - Recommendation Engine

============================================================
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")

# ----------------------------------------------------------
# Load AI Model (Only Once)
# ----------------------------------------------------------

print("Loading AI Search Model...")

model = SentenceTransformer(
    "sentence-transformers/all-mpnet-base-v2"
)

print("Model Loaded.")

# ----------------------------------------------------------
# Connect ChromaDB
# ----------------------------------------------------------

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_collection("ordinex_regulations")

print("Connected to ChromaDB.")
print(f"Loaded {collection.count()} regulations.\n")


# ----------------------------------------------------------
# Search Function
# ----------------------------------------------------------

def search_regulations(query, top_k=5):
    """
    Semantic search over regulations.

    Parameters
    ----------
    query : str

    top_k : int

    Returns
    -------
    list
    """

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []

    ids = results["ids"][0]
    docs = results["documents"][0]
    meta = results["metadatas"][0]

    for i in range(len(ids)):

        matches.append({

            "id": ids[i],

            "country": meta[i]["country"],

            "law": meta[i]["law"],

            "category": meta[i]["category"],

            "risk": meta[i]["risk"],

            "text": docs[i]

        })

    return matches