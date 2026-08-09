from llm import client
from rag import retrieve_chunks


def answer_resume_question(question, top_k=3):

    # --------------------------------------------
    # STEP 1 — Retrieve relevant resume chunks
    # --------------------------------------------

    retrieved_results = retrieve_chunks(
        query=question,
        top_k=top_k
    )

    # --------------------------------------------
    # STEP 2 — Build context
    # --------------------------------------------

    context_parts = []

    for number, result in enumerate(
        retrieved_results,
        start=1
    ):

        context_parts.append(
            f"[Source {number}]\n"
            f"{result['chunk']}"
        )

    context = "\n\n".join(context_parts)

    # --------------------------------------------
    # STEP 3 — Construct grounded prompt
    # --------------------------------------------

    prompt = f"""
You are an AI career assistant analyzing a candidate's resume.

Answer the user's question using ONLY the resume evidence
provided below.

RESUME EVIDENCE:

{context}

USER QUESTION:

{question}

RULES:

1. Base resume-specific claims only on the supplied evidence.

2. Do not invent skills, projects, companies, education,
experience, achievements, or certifications.

3. If the supplied evidence does not contain enough information,
say that the resume does not provide enough evidence.

4. Keep the answer concise and useful.

5. When possible, mention which source supports the answer using
[Source 1], [Source 2], etc.

ANSWER:
"""

    # --------------------------------------------
    # STEP 4 — Send context + question to Groq
    # --------------------------------------------

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded resume analysis assistant. "
                    "Never invent resume information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    # --------------------------------------------
    # STEP 5 — Return answer AND evidence
    # --------------------------------------------

    return {
        "answer": answer,
        "sources": retrieved_results
    }