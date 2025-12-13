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
        courses = edu.get("courses", [])
        courses_text = f" Relevant courses: {', '.join(courses)}." if courses else ""
        
        achievements = edu.get("achievements", [])
        achievements_text = f" Achievements: {', '.join(achievements)}." if achievements else ""
        
        text = (
            f"Education at {safe(edu.get('institution'))}, pursuing {safe(edu.get('degree'))} "
            f"from {safe(edu.get('start_year'))} to {safe(edu.get('expected_graduation'))}. "
            f"GPA: {safe(edu.get('gpa'))}."
            f"{courses_text}{achievements_text}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "education",
                "institution": safe(edu.get("institution"))
            }
        })

    # -----------------------
    # Certifications
    # -----------------------
    for cert in data.get("certifications", []):
        skills_list = cert.get("skills", [])
        skills_text = f" Skills covered: {', '.join(skills_list)}." if skills_list else ""
        
        text = (
            f"Certification: {safe(cert.get('name'))} "
            f"from {safe(cert.get('issuer'))}, "
            f"obtained on {safe(cert.get('date'))}. "
            f"Credential ID: {safe(cert.get('credential_id'))}."
            f"{skills_text}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "certification",
                "name": safe(cert.get("name")),
                "issuer": safe(cert.get("issuer"))
            }
        })

    # -----------------------
    # Awards
    # -----------------------
    for award in data.get("awards", []):
        text = (
            f"Award: {safe(award.get('title'))} "
            f"received on {safe(award.get('date'))} "
            f"from {safe(award.get('issuer'))}. "
            f"Description: {safe(award.get('description'))}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "award",
                "title": safe(award.get("title"))
            }
        })

    # -----------------------
    # Publications
    # -----------------------
    for pub in data.get("publications", []):
        text = (
            f"Publication: {safe(pub.get('title'))} "
            f"in {safe(pub.get('journal'))}, {safe(pub.get('year'))}. "
            f"Summary: {safe(pub.get('summary'))}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "publication",
                "title": safe(pub.get("title"))
            }
        })

    # -----------------------
    # Volunteering
    # -----------------------
    for vol in data.get("volunteering", []):
        responsibilities = vol.get("responsibilities", [])
        resp_text = f" Responsibilities: {', '.join(responsibilities)}." if responsibilities else ""
        
        text = (
            f"Volunteering at {safe(vol.get('organization'))} as {safe(vol.get('role'))} "
            f"from {safe(vol.get('start_date'))} to {safe(vol.get('end_date'))}."
            f"{resp_text}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "volunteering",
                "organization": safe(vol.get("organization"))
            }
        })

    # -----------------------
    # Leadership
    # -----------------------
    for lead in data.get("leadership", []):
        achievements = lead.get("achievements", [])
        achievements_text = f" Achievements: {', '.join(achievements)}." if achievements else ""
        
        text = (
            f"Leadership role: {safe(lead.get('role'))} "
            f"at {safe(lead.get('organization'))} "
            f"from {safe(lead.get('start_date'))} to {safe(lead.get('end_date'))}."
            f"{achievements_text}"
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "leadership",
                "role": safe(lead.get("role"))
            }
        })

    # -----------------------
    # Technical Skills
    # -----------------------
    tech_skills = data.get("technical_skills", {})
    if tech_skills:
        for category, skills_list in tech_skills.items():
            if isinstance(skills_list, list):
                text = f"Technical skills - {category.replace('_', ' ').title()}: {', '.join(skills_list)}."
                chunks.append({
                    "text": text.strip(),
                    "metadata": {
                        "type": "technical_skills",
                        "category": category
                    }
                })

    # -----------------------
    # Languages
    # -----------------------
    for lang in data.get("languages", []):
        text = (
            f"Language: {safe(lang.get('language'))}, "
            f"Proficiency: {safe(lang.get('proficiency'))}."
        )

        chunks.append({
            "text": text.strip(),
            "metadata": {
                "type": "language",
                "language": safe(lang.get("language"))
            }
        })

    # -----------------------
    # Interests
    # -----------------------
    interests = data.get("interests", [])
    if interests:
        text = f"Personal interests include: {', '.join(interests)}."
        chunks.append({
            "text": text.strip(),
            "metadata": {"type": "interests"}
        })

    return chunks
