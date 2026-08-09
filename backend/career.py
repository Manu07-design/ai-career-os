ROLE_SKILLS = {
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "FastAPI",
        "Git",
        "Docker"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "NumPy",
        "Pandas",
        "Machine Learning"
    ],

    "ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "FastAPI",
        "Docker",
        "Git"
    ],

    "Frontend Developer": [
        "JavaScript",
        "React",
        "Git"
    ]
}


def analyze_skill_gap(current_skills, target_role):

    required_skills = ROLE_SKILLS.get(target_role)

    if required_skills is None:
        return None

    missing_skills = []

    for skill in required_skills:
        if skill not in current_skills:
            missing_skills.append(skill)

    score = int(
        ((len(required_skills) - len(missing_skills))
         / len(required_skills)) * 100
    )

    return {
        "target_role": target_role,
        "current_skills": current_skills,
        "required_skills": required_skills,
        "missing_skills": missing_skills,
        "readiness_score": score
    }