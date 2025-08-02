import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

async def job_agent_reply(user_input):
    prompt = f"""
You are JobAgent. Based on the user's interest or career, suggest 3 relevant real-world job titles.

Task:
- List 3 job roles
- For each, give 1 line description and typical employers

User query: {user_input}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()
