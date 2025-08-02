import chainlit as cl
from agents.career_agent import career_agent_reply
from agents.skill_agent import skill_agent_reply
from agents.job_agent import job_agent_reply

@cl.on_chat_start
async def start():
    await cl.Message(content="💼 Hi there! I'm your AI Career Mentor.\n\nTell me about your interests — like your hobbies, favorite subjects, or goals — and I’ll guide you through career options.\n\nYou can say things like:\n- I love coding and building apps.\n- I'm passionate about animals.\n- I enjoy solving logical puzzles.\n\nLet's get started! 😊").send()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content.strip()

    # Detect user intent based on keywords
    if "skill" in user_input.lower():
        reply = await skill_agent_reply(user_input)
    elif "job" in user_input.lower():
        reply = await job_agent_reply(user_input)
    else:
        reply = await career_agent_reply(user_input)

    await cl.Message(content=reply).send()
