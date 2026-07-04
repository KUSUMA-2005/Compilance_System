"""
============================================================
Ordinex AI Compliance System
Cross Encoder Reranker
============================================================

Purpose:
Re-ranks candidate regulations using Cross Encoder
and returns the best regulation with a normalized
confidence score.

Models Used:
- cross-encoder/ms-marco-MiniLM-L-6-v2

============================================================
"""

from sentence_transformers import CrossEncoder
import numpy as np

print("Loading Cross Encoder Model...")

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

print("Cross Encoder Loaded.\n")


def softmax(scores):
    """Convert raw logits into probabilities."""

    scores = np.array(scores)

    exp_scores = np.exp(scores - np.max(scores))

    return exp_scores / exp_scores.sum()


def rerank(policy_clause, candidates):

    if len(candidates) == 0:
        return None

    sentence_pairs = []

    for candidate in candidates:

        sentence_pairs.append(
            (policy_clause, candidate["text"])
        )

    raw_scores = model.predict(sentence_pairs)

    probabilities = softmax(raw_scores)

    # Add score & confidence to every candidate
    for i in range(len(candidates)):
        candidates[i]["raw_score"] = float(raw_scores[i])
        candidates[i]["confidence"] = float(probabilities[i] * 100)

    # Sort candidates by confidence
    ranked_candidates = sorted(
        candidates,
        key=lambda x: x["confidence"],
        reverse=True
    )

    return ranked_candidates[0]