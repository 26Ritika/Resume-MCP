"""
matcher.py
Core logic for comparing a resume against a job description.

Uses:
- Sentence embeddings (all-MiniLM-L6-v2) for semantic similarity
- Simple keyword extraction for "missing skills" detection
"""

import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once at module level (avoids reloading on every call)
_model = SentenceTransformer("all-MiniLM-L6-v2")

# A small curated skill vocabulary — extend this as needed
SKILL_VOCAB = [
    "python", "java", "c++", "javascript", "typescript", "react", "node.js",
    "fastapi", "django", "flask", "sql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "ci/cd",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "langchain", "llm", "rag", "vector database", "chromadb", "pinecone",
    "rest api", "graphql", "websockets", "microservices", "agile",
    "data structures", "algorithms", "leetcode", "system design",
]


def extract_skills(text: str) -> list[str]:
    """Extract known skills mentioned in a text (case-insensitive)."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_VOCAB:
        pattern = re.escape(skill.lower())
        if re.search(r"(?<![a-z])" + pattern + r"(?![a-z])", text_lower):
            found.append(skill)
    return found


def semantic_similarity(resume_text: str, job_description: str) -> float:
    """Return cosine similarity (0-1) between resume and JD embeddings."""
    embeddings = _model.encode([resume_text, job_description])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)


def analyze_match(resume_text: str, job_description: str) -> dict:
    """
    Full analysis: semantic similarity + skill overlap.

    Returns a dict with:
    - similarity_score: 0-100 semantic match
    - matched_skills: skills present in both
    - missing_skills: skills in JD but not in resume
    - extra_skills: skills in resume but not in JD
    """
    sim = semantic_similarity(resume_text, job_description)

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    return {
        "similarity_score": round(sim * 100, 1),
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "jd_skill_count": len(jd_skills),
        "matched_count": len(matched),
    }
