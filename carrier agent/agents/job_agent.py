from agents.base_agent import BaseAgent

def get_job_agent(model):
    return BaseAgent(
        name="JobAgent",
        instructions="You describe real-world job roles and what they involve. Include responsibilities and tools.",
        model=model
    )
