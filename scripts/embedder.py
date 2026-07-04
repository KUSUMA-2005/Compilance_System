"""
=========================================================
Ordinex AI Compliance Engine
Module: Embedding Generator
Author: Team Ordinex
=========================================================

This module:
1. Loads processed regulations
2. Loads the Sentence Transformer model
3. Generates embeddings
4. Saves embeddings and metadata
"""

import json
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA_PATH = (
    BASE_DIR / "Data" / "Processed" / "regulations_processed.json"
)

EMBEDDINGS_FOLDER = BASE_DIR / "Data" / "Embeddings"

EMBEDDINGS_PATH = EMBEDDINGS_FOLDER / "embeddings.npy"

METADATA_PATH = EMBEDDINGS_FOLDER / "metadata.json"


# =========================================================
# Load Processed Regulations
# =========================================================

def load_processed_data():

    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as file:
        regulations = json.load(file)

    return regulations


# =========================================================
# Load AI Model
# =========================================================

def load_model():

    print("\nLoading Sentence Transformer Model...")

    model = SentenceTransformer("all-mpnet-base-v2")

    print("Model Loaded Successfully!\n")

    return model


# =========================================================
# Generate Embeddings
# =========================================================

def generate_embeddings(model, regulations):

    print("Generating embeddings...\n")

    texts = [reg["text"] for reg in regulations]

    start = time.time()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    end = time.time()

    print("\nEmbedding generation completed!")
    print(f"Time Taken : {end-start:.2f} seconds")

    return embeddings


# =========================================================
# Save Embeddings
# =========================================================

def save_embeddings(embeddings, regulations):

    EMBEDDINGS_FOLDER.mkdir(parents=True, exist_ok=True)

    np.save(EMBEDDINGS_PATH, embeddings)

    with open(METADATA_PATH, "w", encoding="utf-8") as file:

        json.dump(regulations, file, indent=4, ensure_ascii=False)

    print("\nEmbeddings Saved Successfully!")

    print(f"Embeddings : {EMBEDDINGS_PATH}")

    print(f"Metadata   : {METADATA_PATH}")


# =========================================================
# Main
# =========================================================

def main():

    print("=" * 60)
    print("ORDINEX AI EMBEDDING GENERATOR")
    print("=" * 60)

    regulations = load_processed_data()

    print(f"\nLoaded {len(regulations)} regulations")

    model = load_model()

    embeddings = generate_embeddings(model, regulations)

    print("\nEmbedding Shape :", embeddings.shape)

    save_embeddings(embeddings, regulations)

    print("\nDone!")

    print("=" * 60)


if __name__ == "__main__":
    main()