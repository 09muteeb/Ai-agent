import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  # For OpenRouter

async def career_agent_reply(user_input):
    prompt = f"""
You are a warm and helpful Career Advisor named CareerAgent.

Task:
- Understand user's interests
- Suggest 3 suitable career fields with 1-2 line explanation each
- Ask if they want a skill roadmap (SkillAgent) or job roles (JobAgent)

User: {user_input}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()
