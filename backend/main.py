from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import io
import re

# ------------------------
# App setup
# ------------------------

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Constants
# ------------------------

SKILLS_DB = [
    "python", "java", "c", "c++", "javascript", "typescript",
    "react", "angular", "node", "spring", "spring boot",
    "sql", "postgresql", "mysql",
    "machine learning", "deep learning",
    "data structures", "algorithms",
    "docker", "kubernetes",
    "aws", "azure", "gcp",
    "fastapi", "rest api", "microservices"
]

ROLE_KEYWORDS = [
    "software development",
    "application development",
    "coding",
    "write code",
    "debug",
    "testing",
    "agile",
    "scrum",
    "version control",
    "git",
    "collaboration",
    "team",
    "problem solving",
    "computer science fundamentals",
    "data structures",
    "algorithms"
]

# ------------------------
# Helper functions
# ------------------------

def clean_text(text: str) -> str:
    text = re.sub(r"\(cid:\d+\)", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def extract_skills(text: str):
    found = []
    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found.append(skill)
    return sorted(set(found))


def extract_role_matches(text: str):
    found = []
    for role in ROLE_KEYWORDS:
        if role in text:
            found.append(role)
    return sorted(set(found))


def tfidf_similarity(text1: str, text2: str) -> int:
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return int(score * 100)


def generate_suggestions(
    missing_skills,
    matched_skills,
    keyword_score,
    semantic_score,
    role_score
):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Consider adding hands-on experience with {skill}.")

    if "fastapi" in matched_skills:
        suggestions.append(
            "Highlight FastAPI backend design, scalability, or performance considerations."
        )

    if keyword_score >= 80:
        suggestions.append(
            "Strong technical skill alignment. Tailor project descriptions to the role."
        )

    if semantic_score < 30:
        suggestions.append(
            "Improve resume summary alignment with the job description language."
        )

    if role_score < 50:
        suggestions.append(
            "Emphasize teamwork, debugging, testing, Agile practices, and CS fundamentals."
        )

    return suggestions

# ------------------------
# API Endpoints
# ------------------------

@app.get("/")
def root():
    return {"status": "Backend is running 🚀"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if resume.content_type != "application/pdf":
        return {"error": "Only PDF resumes are supported"}

    pdf_bytes = await resume.read()

    resume_text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

    clean_resume = clean_text(resume_text)
    clean_job = clean_text(job_description)

    # Skills
    resume_skills = extract_skills(clean_resume)
    job_skills = extract_skills(clean_job)

    matched_skills = set(resume_skills) & set(job_skills)
    missing_skills = list(set(job_skills) - set(resume_skills))

    keyword_score = int(
        (len(matched_skills) / max(len(job_skills), 1)) * 100
    )

    # Semantic match
    semantic_score = tfidf_similarity(clean_resume, clean_job)

    # Role match
    resume_roles = extract_role_matches(clean_resume)
    job_roles = extract_role_matches(clean_job)

    role_match_score = int(
        (len(set(resume_roles) & set(job_roles)) / max(len(job_roles), 1)) * 100
    )

    # Suggestions
    suggestions = generate_suggestions(
        missing_skills,
        matched_skills,
        keyword_score,
        semantic_score,
        role_match_score
    )

    return {
        "keyword_match_score": keyword_score,
        "semantic_match_score": semantic_score,
        "role_match_score": role_match_score,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": list(matched_skills),
        "missing_skills": missing_skills,
        "resume_role_matches": resume_roles,
        "job_role_matches": job_roles,
        "suggestions": suggestions
    }
