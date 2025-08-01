from chainlit import Message, AskAction, Action
from tools.event_generator import generate_event

story_state = {
    "chapter": 0
}

async def handle_narration(message: str):
    story_lines = [
        "🌄 You awaken in a misty forest, a golden key lies beside you.",
        "🏰 You reach an ancient castle with a riddle etched into the door.",
        "🚪 Inside, a spiral staircase leads downward into darkness.",
        "🌋 You descend into a cavern where the walls glow with lava veins.",
        "🎉 You find a legendary sword and a portal glowing ahead."
    ]

    if story_state["chapter"] >= len(story_lines):
        await Message(content="🏁 Your quest has reached its end. Restart to play again.").send()
        return

    current_story = story_lines[story_state["chapter"]]
    story_state["chapter"] += 1

    await Message(content=current_story).send()

    choices = [
        Action(name="explore", value="explore", label="Explore further"),
        Action(name="fight", value="fight", label="Prepare for a fight"),
        Action(name="treasure", value="treasure", label="Search for treasure")
    ]
    await AskAction(message="What do you want to do next?", actions=choices).send()
