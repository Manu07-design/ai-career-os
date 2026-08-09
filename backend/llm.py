import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Add it to your .env file."
    )


client = Groq(api_key=api_key)


def analyze_resume_with_ai(resume_text, skills, target_role):

    prompt = f"""
You are an expert AI career advisor and technical recruiter.

Analyze the candidate's resume for the target role.

TARGET ROLE:
{target_role}

DETECTED SKILLS:
{", ".join(skills) if skills else "No predefined skills detected"}

RESUME:
{resume_text}

Provide a concise but useful analysis with these sections:

1. Resume Summary
2. Strongest Skills
3. Missing or Weak Skills
4. Project Recommendations
5. Resume Improvement Suggestions
6. Next 3 Actions

Do not invent experience that is not present in the resume.
Clearly distinguish between skills demonstrated in the resume and skills
you recommend learning.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a technical recruiter and AI career advisor. "
                    "Base resume-specific claims only on the supplied resume."
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