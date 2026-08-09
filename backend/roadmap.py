from llm import client


def generate_career_roadmap(
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
        else "No major predefined skill gaps detected"
    )

    prompt = f"""
You are an expert AI career mentor.

Create a practical personalized learning roadmap for a candidate.

TARGET ROLE:
{target_role}

CURRENT SKILLS:
{current}

MISSING SKILLS:
{missing}

Create an 8-week roadmap.

For every week provide:

1. Main learning goal
2. Important concepts
3. Practical tasks
4. One project or mini-project
5. Expected outcome

Requirements:

- Prioritize missing skills.
- Do not waste time reteaching skills already demonstrated.
- Make the roadmap realistic.
- Focus on practical engineering.
- Include portfolio-building work.
- Include Git/GitHub usage where appropriate.
- Progress from foundations to production-level work.

At the end provide:

FINAL PORTFOLIO TARGETS

and

INTERVIEW PREPARATION TARGETS
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You create practical technical career roadmaps. "
                    "Avoid generic motivational advice."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content