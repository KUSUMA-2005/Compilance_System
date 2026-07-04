"""
============================================================
Ordinex AI Compliance System
Semantic Search Engine
============================================================

Purpose:
    Converts a user query into an embedding and retrieves
    the most relevant regulations from ChromaDB.

Author: Ordinex Team
============================================================
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")

# ==========================================================
# Load AI Model
# ==========================================================

print("=" * 60)
print("Loading Sentence Transformer Model...")

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

print("Model Loaded Successfully!")

# ==========================================================
# Connect to ChromaDB
# ==========================================================

client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

collection = client.get_collection("ordinex_regulations")

print(f"Connected to ChromaDB")
print(f"Total Regulations : {collection.count()}")

print("=" * 60)


# ==========================================================
# Semantic Search Function
# ==========================================================

def search_regulations(query, top_k=5):
    """
    Searches the vector database using semantic similarity.

    Parameters
    ----------
    query : str
        User query

    top_k : int
        Number of results to return
    """

    print("\nGenerating Query Embedding...\n")

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ==========================================================
# Main Program
# ==========================================================

if __name__ == "__main__":

    while True:

        print("\n")
        print("=" * 60)
        print("AI Compliance Semantic Search")
        print("=" * 60)

        user_query = input("\nEnter your query (type 'exit' to quit): ")

        if user_query.lower() == "exit":
            print("\nGoodbye!")
            break

        results = search_regulations(user_query)

        print("\nTop Matching Regulations\n")

        ids = results["ids"][0]
        documents = results["documents"][0]
        metadata = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):

            similarity = (1 - distances[i]) * 100

            print("=" * 60)
            print(f"Rank       : {i+1}")
            print(f"Reference  : {ids[i]}")
            print(f"Country    : {metadata[i]['country']}")
            print(f"Law        : {metadata[i]['law']}")
            print(f"Category   : {metadata[i]['category']}")
            print(f"Risk Level : {metadata[i]['risk']}")
            print(f"Similarity : {similarity:.2f}%")
            print("\nClause")
            print("-" * 60)
            print(documents[i])
            print("=" * 60)