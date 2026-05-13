def analyze_risk(user_message: str) -> dict:
    message = user_message.lower()

    high_risk_words = [
        "drug", "drugs", "addiction", "addicted", "substance",
        "weed", "alcohol", "smoking", "relapse", "overdose"
    ]

    stress_words = [
        "stress", "stressed", "anxiety", "anxious", "sad",
        "lonely", "angry", "pressure", "tired", "depressed",
        "hopeless", "confused", "fear", "panic"
    ]

    high_count = sum(1 for word in high_risk_words if word in message)
    stress_count = sum(1 for word in stress_words if word in message)

    if high_count > 0:
        return {
            "level": "High Attention",
            "reason": "The message mentions substance-related risk or harmful habits."
        }

    if stress_count >= 2:
        return {
            "level": "Medium Attention",
            "reason": "The message shows emotional stress or pressure."
        }

    if stress_count == 1:
        return {
            "level": "Low Attention",
            "reason": "The message shows mild emotional discomfort."
        }

    return {
        "level": "Stable",
        "reason": "No major emotional or substance-related risk detected."
    }