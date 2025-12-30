def get_ending(profile):
    if profile["logic_bias"] > profile["empathy"]:
        return "AI CONTROL ENDING"
    return "HUMAN FREEDOM ENDING"
