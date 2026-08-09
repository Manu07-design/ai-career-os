from llm import client


def run_career_agent(
    target_role,
    resume_analysis,
    skill_analysis
):

    prompt = f"""
You are the Career Strategy Agent inside an AI Career OS.

TARGET ROLE:
{target_role}

RESUME AGENT FINDINGS:
{resume_analysis}

SKILL AGENT FINDINGS:
{skill_analysis}

Your responsibilities are:

1. Create a practical career strategy.
2. Recommend the highest-value next actions.
3. Recommend portfolio projects.
4. Suggest how the candidate should demonstrate missing skills.
5. Suggest interview preparation priorities.
6. Identify the biggest career-readiness bottleneck.

Do not invent candidate experience.

Return:

CAREER STRATEGY

TOP PRIORITIES

PROJECT RECOMMENDATIONS

INTERVIEW PRIORITIES

BIGGEST BOTTLENECK
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a practical technical career strategist."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content