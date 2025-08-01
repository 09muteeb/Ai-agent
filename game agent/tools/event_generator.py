import random

def generate_event():
    events = [
        "You discover a hidden door behind a waterfall.",
        "A shadowy figure blocks your path.",
        "You find an ancient scroll glowing with magic.",
        "The floor crumbles beneath you!"
    ]
    return random.choice(events)
