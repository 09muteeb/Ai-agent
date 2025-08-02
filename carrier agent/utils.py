def detect_agent_stage(current_stage, message):
    text = message.lower()
    if any(word in text for word in ["skills", "learn", "roadmap"]):
        return "skill"
    elif any(word in text for word in ["job", "salary", "role", "work", "company"]):
        return "job"
    else:
        return "career" if current_stage == "career" else current_stage
