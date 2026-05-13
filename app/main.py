from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.ai_engine import generate_bot_reply
from app.risk_analyzer import analyze_risk

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AI Mental Wellness Companion",
    description="Hackathon project for mental wellness and a drug-free future.",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": "AI Mental Wellness Companion"}
    )


@app.get("/chat")
async def chat_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"app_name": "AI Voice Wellness Bot"}
    )


@app.post("/api/chat")
async def chat_api(chat_request: ChatRequest):
    user_message = chat_request.message.strip()

    if not user_message:
        return {
            "reply": "Please type or speak something so I can support you.",
            "risk_level": "Unknown",
            "reason": "Empty message received."
        }

    return generate_bot_reply(user_message)


@app.get("/checkin")
async def checkin_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="checkin.html",
        context={}
    )


@app.get("/checkin-result")
async def checkin_result(
    request: Request,
    mood: str = "",
    stress: int = 1,
    note: str = ""
):
    combined_text = f"Mood: {mood}. Stress level: {stress}. Note: {note}"
    risk = analyze_risk(combined_text)

    if stress >= 8:
        guidance = (
            "Your stress level looks high. Pause for a moment, take slow breaths, "
            "move away from pressure, and speak to someone you trust today."
        )
    elif stress >= 5:
        guidance = (
            "You may be under moderate pressure. Try a short walk, water, deep breathing, "
            "and avoid unhealthy coping choices."
        )
    else:
        guidance = (
            "Your current check-in looks stable. Keep building healthy habits and stay connected "
            "with supportive people."
        )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "mood": mood,
            "stress": stress,
            "note": note,
            "risk_level": risk["level"],
            "reason": risk["reason"],
            "guidance": guidance
        }
    )


@app.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={}
    )


@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "message": "Backend is working properly"
    }