import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create OpenAI client (works for OpenRouter too if base_url is given)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# Keep track of chat history
messages = [
    {
        "role": "system",
        "content": "You are a helpful AI Travel Agent. Greet the user, ask about their travel mood or interests, and suggest travel destinations, hotels, and attractions."
    }
]

# Handle incoming user messages
@cl.on_message
async def on_message(msg: cl.Message):
    messages.append({"role": "user", "content": msg.content})

    # Make API call to OpenRouter (OpenAI-compatible)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    # Send reply back to Chainlit UI
    await cl.Message(content=reply).send()
