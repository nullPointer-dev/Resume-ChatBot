"""
Lightweight text embedding and similarity module.

This module provides:
- Tokenization
- Bag-of-words embedding (word frequency vector)
- Cosine similarity scoring

Used by the vector store for simple, fast semantic search.
"""

import math
import re
from collections import Counter
from typing import Dict, List


# ----------------------------------------------
# Text Preprocessing
# ----------------------------------------------
def tokenize(text: str) -> List[str]:
    """
    Convert a text string into normalized tokens.

    - Lowercases text
    - Removes non-alphanumeric characters
    - Splits into tokens

    Args:
        text: Raw input text

    Returns:
        List of processed tokens
    """
    cleaned = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return cleaned.split()


# ----------------------------------------------
# Embedding Function
# ----------------------------------------------
def embed_text(text: str) -> Dict[str, int]:
    """
    Create a simple bag-of-words embedding using term frequency.

    Args:
        text: Input text to embed

    Returns:
        A dictionary mapping token -> count
        (Acts as a sparse vector)
    """
    tokens = tokenize(text)
    return Counter(tokens)


# ----------------------------------------------
# Cosine Similarity
# ----------------------------------------------
def cosine_similarity(vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
    """
    Compute cosine similarity between two sparse BoW vectors.

    Args:
        vec1: First embedding vector
        vec2: Second embedding vector

    Returns:
        Cosine similarity (0.0–1.0)
    """

    # Dot product
    dot = sum(count * vec2.get(token, 0) for token, count in vec1.items())

    # Magnitudes
    mag1 = math.sqrt(sum(count * count for count in vec1.values()))
    mag2 = math.sqrt(sum(count * count for count in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return dot / (mag1 * mag2)
