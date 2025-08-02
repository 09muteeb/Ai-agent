import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

async def skill_agent_reply(user_input):
    prompt = f"""
You are SkillAgent. Based on the user's interest or career, provide a skill roadmap.

Task:
- Mention 5–7 essential skills/tools/concepts to learn
- Organize them in steps
- Keep it encouraging and structured

User request: {user_input}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()
