from app.risk_analyzer import analyze_risk


def generate_bot_reply(user_message: str) -> dict:
    risk = analyze_risk(user_message)

    message = user_message.lower()

    if risk["level"] == "High Attention":
        reply = (
            "I hear you. It sounds like this may be connected to substance pressure or harmful habits. "
            "A strong first step is to pause, avoid being alone with the trigger, and talk to a trusted person. "
            "You are not weak for asking for support. Choose one safe action now: drink water, move away from the trigger, "
            "call someone you trust, or write down what you are feeling."
        )

    elif risk["level"] == "Medium Attention":
        reply = (
            "It sounds like you are carrying a lot of pressure. Before reacting, take one slow breath and name what you are feeling. "
            "Try one small reset: walk for two minutes, drink water, or message someone you trust. "
            "You do not have to handle everything alone."
        )

    elif risk["level"] == "Low Attention":
        reply = (
            "Thanks for sharing that. Your feeling is valid. Try to slow things down and focus on one helpful action right now. "
            "A short break, a calm breath, or writing your thoughts can help you understand what you need next."
        )
#else 
    else:
        reply = (
            "I am glad you checked in. Staying aware of your emotions is a strong habit. "
            "Keep choosing healthy coping actions and stay connected with people who support your growth."
        )

    if "exam" in message or "study" in message:
        reply += " For study pressure, split your work into a 25-minute focus block and one 5-minute break."

    if "friend" in message or "peer" in message:
        reply += " If peer pressure is involved, prepare a simple line like: 'No, I am not doing that. I have other goals.'"

    return {
        "reply": reply,
        "risk_level": risk["level"],
        "reason": risk["reason"]
    }