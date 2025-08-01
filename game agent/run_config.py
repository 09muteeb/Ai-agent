from agents.narrator import handle_narration
from agents.monster import handle_monster_encounter
from agents.item import handle_item_reward

# Message router based on user choice
async def route_message(message: str):
    lowered = message.lower()

    if lowered in ["start", "explore"]:
        await handle_narration(message)
    elif lowered == "fight":
        await handle_monster_encounter(message)
    elif lowered == "treasure":
        await handle_item_reward(message)
    else:
        # If the input is not understood
        await handle_narration("continue")
