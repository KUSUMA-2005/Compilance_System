"""
============================================================
Ordinex AI Compliance System
Matcher Engine
============================================================

Purpose:
    Finds the best matching regulation for a given
    company policy clause using:

    1. Semantic Search (Sentence Transformer)
    2. AI Re-ranking (Cross Encoder)

Models Used:
    • sentence-transformers/all-mpnet-base-v2
    • cross-encoder/ms-marco-MiniLM-L-6-v2

Author:
    Ordinex Team

============================================================
"""

from search_service import search_regulations
from reranker import rerank


def get_confidence_level(confidence_score):
    """
    Converts confidence percentage into
    a human-readable confidence level.
    """

    if confidence_score >= 90:
        return "Excellent"

    elif confidence_score >= 75:
        return "High"

    elif confidence_score >= 60:
        return "Medium"

    else:
        return "Low"


def find_best_match(policy_clause):
    """
    Finds the best regulation for a given policy clause.

    Parameters
    ----------
    policy_clause : str

    Returns
    -------
    dict
        Best matching regulation
    """

    # Retrieve Top 5 regulations
    candidates = search_regulations(
        policy_clause,
        top_k=5
    )

    # AI Re-ranking
    best_match = rerank(
        policy_clause,
        candidates
    )

    return best_match


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print(" ORDINEX AI - MULTI-COUNTRY REGULATION MATCHER ")
    print("=" * 70)

    clause = input("\nEnter Company Policy Clause:\n\n")

    match = find_best_match(clause)

    if match is None:
        print("\nNo matching regulation found.")
        exit()

    print("\n")
print("=" * 70)
print(" COMPANY POLICY ANALYSIS ")
print("=" * 70)

print("\nAnalysis Completed Successfully")
print("AI Retrieval Status : SUCCESS")

print("\nBest Matching Regulation")
print("-" * 70)

print(f"Reference      : {match['id']}")
print(f"Country        : {match['country']}")
print(f"Law            : {match['law']}")
print(f"Category       : {match['category']}")
print(f"Risk Level     : {match['risk']}")

print("\nMatched Regulation")
print("-" * 70)
print(match["text"])

print("=" * 70)