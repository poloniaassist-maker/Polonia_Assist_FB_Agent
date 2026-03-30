from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Klucz OpenAI z ENV (Render → Environment → OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.get("/")
def home():
    return {
        "status": "ok",
        "message": "Polonia Assist Agent działa z OpenAI"
    }


# -------------------------
# BAZA WIEDZY POLONIA ASSIST
# -------------------------
# Możesz ją dowolnie rozszerzać.
# Agent korzysta TYLKO z tych danych.
knowledge_base = {
    "umowa": {
        "content": (
            "Umowy w Holandii muszą być zgodne z właściwym CAO i zawierać: stawkę, liczbę godzin, "
            "okres próbny, zasady dodatków, informacje o zakwaterowaniu i kosztach. "
            "Polonia Assist analizuje umowy i wskazuje nieprawidłowości."
        ),
        "url": "https://www.poloniaassist.nl/umowy"
    },
    "bsn": {
        "content": (
            "BSN wymaga meldunku lub tymczasowego adresu. Każda gmina ma inne wymagania. "
            "Polonia Assist pomaga w sytuacjach, gdy pracodawca odmawia adresu lub pojawiają się problemy z rejestracją."
        ),
        "url": "https://www.poloniaassist.nl/bsn"
    },
    "snf": {
        "content": (
            "Zakwaterowanie SNF musi spełniać normy i mieścić się w limitach potrąceń. "
            "Polonia Assist analizuje umowy mieszkaniowe i payslipy pod kątem nieprawidłowości."
        ),
        "url": "https://www.poloniaassist.nl/zakwaterowanie-snf"
    },
    "payslip": {
        "content": (
            "Wypłaty w Holandii muszą być zgodne z WML i CAO. Najczęstsze błędy to złe dodatki, "
            "nieprawidłowe potrącenia i błędne naliczanie godzin. Polonia Assist analizuje payslipy."
        ),
        "url": "https://www.poloniaassist.nl/payslip"
    }
}


# -------------------------
# MODELE WEJŚCIA
# -------------------------
class PostInput(BaseModel):
    text: str


# -------------------------
# FUNKCJA: WYSZUKIWANIE WIEDZY
# -------------------------
def search_knowledge(text: str):
    text_lower = text.lower()
    for key, data in knowledge_base.items():
        if key in text_lower:
            return data
    return None


# -------------------------
# FUNKCJA: GENEROWANIE ODPOWIEDZI OPENAI
# -------------------------
def generate_ai_reply(user_text: str, knowledge: dict | None):
    if knowledge:
        # Odpowiedź oparta na bazie wiedzy Polonia Assist
        prompt = f"""
Jesteś ekspertem Polonia Assist. Odpowiadasz rzeczowo, konkretnie, po polsku.
Zawsze subtelnie podkreślasz, że Polonia Assist może pomóc w danym temacie.
Nie korzystasz z żadnych źródeł poza bazą wiedzy poniżej.

BAZA WIEDZY:
{knowledge['content']}

LINK DO ŹRÓDŁA:
{knowledge['url']}

UŻYTKOWNIK PYTA:
{user_text}

ODPOWIEDŹ W STYLU POLONIA ASSIST:
"""
    else:
        # Wersja robocza, gdy brak danych w bazie
        prompt = f"""
Jesteś ekspertem Polonia Assist. Odpowiadasz rzeczowo, konkretnie, po polsku.
Nie masz danych w bazie wiedzy, więc generujesz wersję roboczą odpowiedzi.
Na końcu dodaj zdanie:
"Jeśli chcesz, mogę przygotować pełną odpowiedź, gdy tylko podasz więcej szczegółów."

UŻYTKOWNIK PYTA:
{user_text}

ODPOWIEDŹ ROBOCZA:
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Jesteś ekspertem Polonia Assist."},
                  {"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message["content"]


# -------------------------
# ENDPOINT GŁÓWNY
# -------------------------
@app.post("/analyze")
def analyze_post(data: PostInput):
    knowledge = search_knowledge(data.text)
    reply = generate_ai_reply(data.text, knowledge)

    return {
        "received_text": data.text,
        "agent_reply": reply,
        "source": knowledge["url"] if knowledge else None
    }
from fastapi import Request
import httpx

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")


@app.get("/facebook/webhook")
async def verify_facebook(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return {"status": "error", "message": "Invalid verification token"}


@app.post("/facebook/webhook")
async def facebook_webhook(request: Request):
    data = await request.json()

    # Facebook wysyła różne typy eventów — interesują nas komentarze
    if "entry" in data:
        for entry in data["entry"]:
            if "changes" in entry:
                for change in entry["changes"]:
                    if change.get("field") == "feed":
                        value = change.get("value", {})
                        if value.get("item") == "comment" and "message" in value:
                            comment_text = value["message"]
                            comment_id = value["comment_id"]

                            # Generujemy odpowiedź przez nasz endpoint analyze
                            reply = generate_ai_reply(comment_text, search_knowledge(comment_text))

                            # Wysyłamy odpowiedź na Facebooka
                            await send_facebook_reply(comment_id, reply)

    return {"status": "ok"}


async def send_facebook_reply(comment_id: str, message: str):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/comments"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {"message": message}

    async with httpx.AsyncClient() as client:
        await client.post(url, params=params, json=payload)
from cron import run_agent_cycle

@app.get("/test-cron")
def test_cron():
    run_agent_cycle()
    return {"status": "agent executed"}
