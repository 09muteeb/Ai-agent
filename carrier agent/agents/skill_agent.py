from agents.base_agent import BaseAgent

def get_skill_agent(model):
    return BaseAgent(
        name="SkillAgent",
        instructions="You explain the skills needed for a specific career path in a roadmap format.",
        model=model
    )
