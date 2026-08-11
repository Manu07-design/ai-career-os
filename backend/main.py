from fastapi import FastAPI, UploadFile, HTTPException
import os

from parser import parse_resume
from skills import extract_skills
from career import analyze_skill_gap
from llm import analyze_resume_with_ai
from roadmap import generate_career_roadmap
from rag import build_vector_store, retrieve_chunks
from rag_chat import answer_resume_question
from agents.orchestrator import run_career_team
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="AI Career OS API",
    description="AI-powered career intelligence and resume analysis platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://ai-career-2j4jhqiaz-manus-projects-696460a1.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


# Temporary in-memory resume storage
# Later we will replace this with proper user/session storage.
resume_data = {
    "text": "",
    "skills": []
}


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Career OS API is running",
        "version": "1.0.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

@app.post("/upload")
async def upload_resume(file: UploadFile):

    # Only allow PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are currently supported."
        )

    # Create safe file path
    file_path = os.path.join(
        UPLOAD_DIR,
        os.path.basename(file.filename)
    )

    # Read uploaded file
    content = await file.read()

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(content)

    # Extract resume text
    resume_text = parse_resume(file_path)
    print("=" * 60)
    print(resume_text)
    print("=" * 60)

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text could be extracted from the PDF."
        )

    # Extract skills
    skills = extract_skills(resume_text)
    print("=" * 50)
    print("Extracted Skills:")
    print(skills)
    print("=" * 50)

    # Store temporarily
    resume_data["text"] = resume_text
    resume_data["skills"] = skills
    vector_info = build_vector_store(resume_text)

    return {
        "status": "success",
        "filename": file.filename,
        "skills": skills,
        "vector_store": vector_info,
        "preview": resume_text[:500]
    }


# --------------------------------------------------
# RULE-BASED SKILL GAP ANALYSIS
# --------------------------------------------------

@app.get("/analyze")
def analyze(target_role: str):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail="Upload a resume before requesting analysis."
        )

    result = analyze_skill_gap(
        resume_data["skills"],
        target_role
    )

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Target role is not currently supported."
        )

    return result


# --------------------------------------------------
# AI-POWERED RESUME ANALYSIS
# --------------------------------------------------

@app.get("/ai-analysis")
def ai_analysis(target_role: str):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail="Upload a resume before requesting AI analysis."
        )

    analysis = analyze_resume_with_ai(
        resume_text=resume_data["text"],
        skills=resume_data["skills"],
        target_role=target_role
    )

    return {
        "target_role": target_role,
        "analysis": analysis
    }
@app.get("/roadmap")
def roadmap(target_role: str):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail="Upload a resume before generating a roadmap."
        )

    skill_analysis = analyze_skill_gap(
        resume_data["skills"],
        target_role
    )

    if skill_analysis is None:
        raise HTTPException(
            status_code=400,
            detail="Target role is not currently supported."
        )

    generated_roadmap = generate_career_roadmap(
        current_skills=resume_data["skills"],
        missing_skills=skill_analysis["missing_skills"],
        target_role=target_role
    )

    return {
        "target_role": target_role,
        "readiness_score": skill_analysis["readiness_score"],
        "current_skills": resume_data["skills"],
        "missing_skills": skill_analysis["missing_skills"],
        "roadmap": generated_roadmap
    }
@app.get("/retrieve")
def retrieve(query: str, top_k: int = 3):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail="Upload a resume before searching it."
        )

    if top_k < 1 or top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10."
        )

    try:

        results = retrieve_chunks(
            query=query,
            top_k=top_k
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "query": query,
        "results": results
    }
@app.get("/chat")
def chat(question: str, top_k: int = 3):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail="Upload a resume before using career chat."
        )

    if top_k < 1 or top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10."
        )

    try:

        result = answer_resume_question(
            question=question,
            top_k=top_k
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
@app.get("/career-team")
def career_team(target_role: str):

    if not resume_data["text"]:
        raise HTTPException(
            status_code=400,
            detail=(
                "Upload a resume before running "
                "the career intelligence team."
            )
        )

    try:

        report = run_career_team(
            resume_text=resume_data["text"],
            current_skills=resume_data["skills"],
            target_role=target_role
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return report
