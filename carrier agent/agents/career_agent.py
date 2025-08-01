from agents.base_agent import BaseAgent

def get_career_agent(model):
    return BaseAgent(
        name="CareerAgent",
        instructions="You help users explore career fields based on their interests. Be friendly and insightful.",
        model=model
    )
