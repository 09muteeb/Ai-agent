from agents import Agent

class BaseAgent(Agent):
    def __init__(self, name, instructions, model):
        super().__init__(name=name, instructions=instructions, model=model)
