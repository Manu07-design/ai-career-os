from llm import client


def run_resume_agent(resume_text):

    prompt = f"""
You are the Resume Analysis Agent inside an AI Career OS.

Analyze the resume below.

RESUME:
{resume_text}

Your responsibilities are ONLY:

1. Summarize the candidate's technical profile.
2. Identify demonstrated technical strengths.
3. Identify notable projects.
4. Identify weaknesses in resume presentation.
5. Identify missing evidence or unclear claims.

Do not create a career roadmap.
Do not invent experience.
Do not assume skills that are not supported by the resume.

Return a concise professional analysis.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a technical resume analyst. "
                    "Only make candidate-specific claims supported "
                    "by the provided resume."
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