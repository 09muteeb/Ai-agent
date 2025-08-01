import chainlit as cl
from run_config import route_message

@cl.on_chat_start
async def start():
    await cl.Message(
        content="🎮 Welcome to the Fantasy Adventure Game!\nType or click 'Start' to begin your journey.",
        actions=[cl.Action(name="start_game", value="start", label="Start Game")]
    ).send()

@cl.on_action
async def on_action(action: cl.Action):
    await route_message(action.value)

@cl.on_message
async def on_message(message: cl.Message):
    await route_message(message.content)
