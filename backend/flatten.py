import json
import os
from typing import Any, Dict, List


# ------------------------------------------------------
# Load resume JSON
# ------------------------------------------------------
def load_resume_json(path: str = "example_resume.json") -> Dict[str, Any]:
    """
    Load resume JSON from disk.

    Parameters:
        path (str): Path to the resume JSON file.

    Returns:
        dict: Parsed resume JSON.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------
# Safe extractor
# ------------------------------------------------------
def safe(value: Any) -> str:
    """Convert None → empty string to avoid weird text like 'None'."""
    return value if value is not None else ""


# ------------------------------------------------------
# Flatten resume into embedding-friendly text chunks
# ------------------------------------------------------
def flatten_resume(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert structured resume JSON into a list of text chunks suitable
    for embedding + retrieval.

    Each chunk contains:
    - text (str): A natural-language description of a resume section
    - metadata (dict): Structured info identifying the section
    """

    chunks: List[Dict[str, Any]] = []

    # -----------------------
    # Basics section
    # -----------------------
    basics = data.get("basics", {})
    basics_text = (
        f"Name: {safe(basics.get('name'))}. "
        f"Headline: {safe(basics.get('headline'))}. "
        f"Email: {safe(basics.get('email'))}. "
        f"Location: {safe(basics.get('location'))}. "
        f"Summary: {safe(basics.get('summary'))}."
    )

    chunks.append({
        "text": basics_text.strip(),
        "metadata": {"type": "basics"}
    })

    # -----------------------
    # Skills
    # -----------------------
    skills = data.get("skills", [])
    if skills:
        skills_text = f"Skills include: {', '.join(skills)}."
        chunks.append({
            "text": skills_text,
            "metadata": {"type": "skills"}
        })

    # -----------------------
    # Experience
    # -----------------------
    for exp in data.get("experience", []):
        achievements = exp.get("achievements", [])
        achievements_text = ", ".join(achievements) if achievements else "No listed achievements"

        text = (
            f"Experience at {safe(exp.get('company'))} as {safe(exp.get('role'))} "
            f"from {safe(exp.get('start_date'))} to {safe(exp.get('end_date'))}. "
            f"Achievements: {achievements_text}."
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "experience",
                "company": safe(exp.get("company"))
            }
        })

    # -----------------------
    # Projects
    # -----------------------
    for proj in data.get("projects", []):
        tech_stack = proj.get("tech", [])
        tech_text = ", ".join(tech_stack) if tech_stack else "No technologies specified"

        text = (
            f"Project: {safe(proj.get('name'))}. "
            f"Technologies used: {tech_text}. "
            f"Description: {safe(proj.get('description'))}."
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "project",
                "name": safe(proj.get("name"))
            }
        })

    # -----------------------
    # Education
    # -----------------------
    for edu in data.get("education", []):
        text = (
            f"Education at {safe(edu.get('institution'))}, pursuing {safe(edu.get('degree'))} "
            f"from {safe(edu.get('start_year'))} to {safe(edu.get('expected_graduation'))}."
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "education",
                "institution": safe(edu.get("institution"))
            }
        })

    return chunks
