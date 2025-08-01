from chainlit import Message
from tools.dice_roller import roll_dice

async def handle_monster_encounter(message: str):
    await Message(content="👹 A wild ogre appears and charges toward you!").send()
    roll = roll_dice(12)

    if roll >= 8:
        result = f"You strike the ogre with your blade and defeat it! 🎯 (Roll: {roll})"
    else:
        result = f"The ogre overpowers you. You barely escape! 🏃 (Roll: {roll})"

    await Message(content=result).send()
