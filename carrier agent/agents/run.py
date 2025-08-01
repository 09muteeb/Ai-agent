from agents import RunConfig

def build_run_config(model, provider):
    return RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True
    )
