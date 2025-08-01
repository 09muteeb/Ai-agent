# run_config.py

from chainlit.config import RunConfig
from chainlit.input_widget import Select
from chainlit.server.settings import settings

settings.project.custom_name = "AI Travel Agent"

config = RunConfig(
    user_env_vars=[
        Select(
            id="model",
            label="Select a model",
            values=["openrouter/gpt-3.5-turbo", "openrouter/gpt-4", "openrouter/mistral"],
            initial_index=0
        )
    ]
)
