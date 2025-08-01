import os
import chainlit as cl
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message("👋 Hi! I'm your Career Mentor AI. Ask me about careers, skills, or job guidance!").send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")

    messages = [
        {
            "role": "system",
            "content": (
                "You're a helpful, human-like Career Mentor AI. You guide users about career paths, job opportunities, and learning skills."
            )
        }
    ]

    for turn in history:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["bot"]})

    messages.append({"role": "user", "content": message.content})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Use gpt-3.5-turbo instead of gpt-4
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"❌ OpenAI Error: {str(e)}"

    history.append({"user": message.content, "bot": answer})
    cl.user_session.set("history", history)

    await cl.Message(content=answer).send()
