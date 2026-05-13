import os
from google import genai
from dotenv import load_dotenv

from app.risk_analyzer import analyze_risk

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_bot_reply(user_message: str) -> dict:
    risk = analyze_risk(user_message)

    prompt = f"""
You are AURA, an AI mental wellness companion for a drug-free future.

User message:
{user_message}

Risk analysis:
Level: {risk["level"]}
Reason: {risk["reason"]}

Rules:
- Give short, calm, supportive guidance.
- Do not give medical diagnosis.
- Do not encourage drug use or harmful behavior.
- If the user mentions peer pressure, stress, harmful habits, or substances, guide them toward safe coping choices.
- If the user seems seriously distressed, suggest speaking to a trusted adult, counselor, teacher, guardian, or local emergency support.
- Keep the reply under 90 words.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        reply = response.text or "I am here with you. Try one calm step now: breathe slowly, drink water, and talk to someone you trust."

    except Exception:
        reply = (
            "I am here with you. I could not connect to the AI model right now, "
            "but you can still take one safe step: pause, breathe slowly, drink water, "
            "and talk to someone you trust."
        )

    return {
        "reply": reply,
        "risk_level": risk["level"],
        "reason": risk["reason"]
    }