from chainlit import Message
import random

async def handle_item_reward(message: str):
    rewards = [
        "🧪 You find a glowing health potion and restore your strength.",
        "💎 A hidden chest contains rare jewels.",
        "🗡️ You pick up a magical dagger with frost enchantments.",
        "📜 You find a spell scroll written in an ancient language."
    ]
    await Message(content=random.choice(rewards)).send()
