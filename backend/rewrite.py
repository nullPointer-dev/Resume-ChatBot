import re
from typing import List, Tuple


# ----------------------------------------
# First-person rewrite helper
# ----------------------------------------
def to_first_person(text: str) -> str:
    """
    Convert third-person resume text into clean first-person language.
    Only rewrites narrative lines—not fields like 'Name:', 'Email:', etc.

    Parameters:
    - text (str): The original text chunk.

    Returns:
    - str: Rewritten text in first-person tone.
    """

    # Skip rewriting metadata-like fields
    if text.strip().lower().startswith(
        ("name:", "email:", "location:", "headline:", "summary:")
    ):
        return text.strip()

    # Ordered replacements (case-sensitive + case-insensitive versions)
    replacements: List[Tuple[str, str]] = [
        (r"\bShashank\b", "I"),
        (r"\bHe\b", "I"), (r"\bhe\b", "I"),
        (r"\bHis\b", "My"), (r"\bhis\b", "my"),
        (r"\bYour\b", "My"), (r"\byour\b", "my"),
        (r"\bYou\b", "I"), (r"\byou\b", "I"),
    ]

    rewritten = text

    # Apply regex substitutions
    for pattern, replacement in replacements:
        rewritten = re.sub(pattern, replacement, rewritten)

    return rewritten.strip()
