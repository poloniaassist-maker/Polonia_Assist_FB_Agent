from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "message": "Polonia Assist Agent działa"}

from pydantic import BaseModel

class PostInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_post(data: PostInput):
    # Tu później dodamy AI, Facebooka, WIX itd.
    # Na razie zwrócimy prostą odpowiedź testową.
    return {
        "received_text": data.text,
        "agent_reply": f"Otrzymałem tekst: {data.text}. Wkrótce wygeneruję odpowiedź!"
    }
