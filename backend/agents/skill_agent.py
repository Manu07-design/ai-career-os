from llm import client


def run_skill_agent(
    current_skills,
    missing_skills,
    target_role
):

    current = (
        ", ".join(current_skills)
        if current_skills
        else "No predefined skills detected"
    )

    missing = (
        ", ".join(missing_skills)
        if missing_skills
        else "No predefined gaps detected"
    )

    prompt = f"""
You are the Skill Gap Analysis Agent inside an AI Career OS.

TARGET ROLE:
{target_role}

CURRENT DETECTED SKILLS:
{current}

CURRENTLY IDENTIFIED SKILL GAPS:
{missing}

Your responsibilities are ONLY:

1. Evaluate the candidate's technical readiness.
2. Prioritize the missing skills.
3. Explain why the most important gaps matter.
4. Identify which existing skills are useful for the target role.
5. Recommend the next technical competencies to prove through projects.

Do not write a weekly learning roadmap.
Do not analyze resume formatting.
Do not invent candidate experience.

Return a concise technical skill-gap analysis.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a technical skill-gap analyst."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content