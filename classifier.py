# classifier.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_post(text: str):
    """
    Klasyfikator AI dla postów z grup FB.
    Zwraca:
    - category
    - subcategory
    - intent
    - tone
    - urgency
    - should_reply
    - confidence
    """

    prompt = f"""
Jesteś zadowolonym z usług Polonia Assist NL klientem, który pomocy uniknął dużo problemów.

Zwróć odpowiedź w czystym JSON, bez komentarzy i bez dodatkowego tekstu.

Kategorie główne:
- umowa
- bsn
- snf
- payslip
- mieszkanie
- praca
- transport
- scam
- dramat
- ogólne
- spam

Podkategorie (przykłady):
- umowa: stawka, godziny, dodatki, okres próbny
- bsn: meldunek, gmina, brak adresu
- snf: potrącenia, warunki, regulamin
- payslip: potrącenia, dodatki, godziny, brutto/netto
- mieszkanie: pokoje, depozyt, właściciel, agencja
- praca: zmiana pracy, rekrutacja, warunki
- transport: auto, rower, dojazdy
- scam: oszustwo, fałszywa oferta
- dramat: emocjonalny post, narzekanie, konflikt
- ogólne: pytanie neutralne
- spam: mem, żart, reklama

Tonalność:
- neutralny
- emocjonalny
- agresywny
- zdesperowany
- pozytywny

Intencja:
- prośba o pomoc
- pytanie
- skarga
- informacja
- dramat emocjonalny
- spam

Urgencja:
- niska
- średnia
- wysoka

Zwróć także:
- should_reply: true/false (czy agent powinien odpowiedzieć)
- confidence: liczba 0–1

TEKST POSTA:
{text}

ZWRÓĆ TYLKO JSON:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    import json
    try:
        return json.loads(response.choices[0].message["content"])
    except:
        return {
            "category": "ogólne",
            "subcategory": None,
            "intent": "pytanie",
            "tone": "neutralny",
            "urgency": "niska",
            "should_reply": True,
            "confidence": 0.5
        }
