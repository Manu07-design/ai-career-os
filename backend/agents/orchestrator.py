from agents.resume_agent import run_resume_agent
from agents.skill_agent import run_skill_agent
from agents.career_agent import run_career_agent

from career import analyze_skill_gap


def run_career_team(
    resume_text,
    current_skills,
    target_role
):

    # ---------------------------------------------
    # 1. Deterministic skill-gap analysis
    # ---------------------------------------------

    gap_result = analyze_skill_gap(
        current_skills,
        target_role
    )

    if gap_result is None:
        raise ValueError(
            "Target role is not currently supported."
        )

    missing_skills = gap_result["missing_skills"]

    # ---------------------------------------------
    # 2. Resume Agent
    # ---------------------------------------------

    resume_analysis = run_resume_agent(
        resume_text
    )

    # ---------------------------------------------
    # 3. Skill Agent
    # ---------------------------------------------

    skill_analysis = run_skill_agent(
        current_skills=current_skills,
        missing_skills=missing_skills,
        target_role=target_role
    )

    # ---------------------------------------------
    # 4. Career Strategy Agent
    # ---------------------------------------------

    career_strategy = run_career_agent(
        target_role=target_role,
        resume_analysis=resume_analysis,
        skill_analysis=skill_analysis
    )

    # ---------------------------------------------
    # 5. Return combined report
    # ---------------------------------------------

    return {
        "target_role": target_role,

        "readiness_score": gap_result[
            "readiness_score"
        ],

        "current_skills": current_skills,

        "missing_skills": missing_skills,

        "resume_agent": resume_analysis,

        "skill_agent": skill_analysis,

        "career_agent": career_strategy
    }