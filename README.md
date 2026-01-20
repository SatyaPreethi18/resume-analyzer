# AI Resume Analyzer (Role-Aware, ATS-Inspired)

A full-stack resume analysis tool that evaluates how well a resume aligns with a job description by combining deterministic skill matching, role-based responsibility analysis, and semantic similarity scoring.

Unlike typical AI-only resume analyzers, this system prioritizes explainability, correctness, and real-world hiring behavior.

---

## 🔍 Why This Project?

Most resume analyzers rely entirely on large language models that:
- Hallucinate skills
- Inflate match scores
- Cannot explain *why* a score was given

In real hiring systems (ATS and enterprise recruitment), decisions are:
- Rule-based
- Deterministic
- Explainable

This project mirrors that reality.

---

## 🧠 Key Features

### 1. Resume Parsing
- Upload resume as PDF
- Extracts and cleans unstructured text

### 2. Skill-Based Matching (ATS-style)
- Matches explicit technical skills against job requirements
- Produces a deterministic keyword match score
- Does **not** infer or hallucinate skills

### 3. Role-Aware Matching
- Detects job responsibilities such as:
  - Debugging
  - Testing
  - Agile collaboration
  - Computer science fundamentals
- Ensures entry-level and enterprise roles are evaluated fairly

### 4. Semantic Similarity
- Uses TF-IDF + cosine similarity
- Measures overall contextual alignment
- Acts as a secondary signal, not a decision-maker

### 5. Actionable Suggestions
- Highlights missing skills (if any)
- Suggests resume improvements based on role expectations
- Explains low scores instead of hiding them

### 6. Frontend Interface
- Upload resume
- Paste job description
- View scores, matches, and suggestions instantly

---

## 🏗️ Architecture Overview

Frontend (React)
|
| multipart/form-data
v
Backend (FastAPI)
├── PDF Parsing
├── Text Cleaning
├── Skill Matching
├── Role Matching
├── Semantic Scoring
└── Suggestions Engine


---

## ⚙️ Tech Stack

**Frontend**
- React
- Fetch API

**Backend**
- Python
- FastAPI
- pdfplumber
- scikit-learn (TF-IDF)

---

## 📊 Example Behavior (IBM Entry-Level JD)

- Keyword Match: Low or 0% (no explicit tools listed)
- Role Match: High (focus on fundamentals, teamwork, delivery)
- Suggestions:
  - Improve resume narrative
  - Emphasize debugging, testing, Agile collaboration

This reflects real enterprise hiring logic.

---

## 🚫 What This Project Does NOT Do

- Does not hallucinate skills
- Does not inflate match scores
- Does not rely solely on AI-generated feedback

AI is intentionally reserved for future language-based enhancements.

---

## 🔮 Future Improvements

- AI-assisted resume bullet rewriting
- Multi-job comparison for a single resume
- Analysis history and persistence
- Embeddings-based semantic similarity

---

## 🧑‍💻 Author

Built as a portfolio project to demonstrate practical system design, explainable decision-making, and full-stack development skills.
