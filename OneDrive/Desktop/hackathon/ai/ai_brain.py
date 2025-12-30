from ai.ai_profile import ai_profile

def evaluate_choice(key):
    if key in ai_profile:
        ai_profile[key] += 1
        print("AI PROFILE:", ai_profile)
