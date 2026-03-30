# generate_reply.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(classification: dict, text: str):
    """
    Generuje inteligentną odpowiedź na podstawie:
    - klasyfikacji posta
    - treści posta
    - stylu Polonia Assist
    """

    category = classification.get("category", "ogólne")
    intent = classification.get("intent", "pytanie")
    tone = classification.get("tone", "neutralny")
    urgency = classification.get("urgency", "niska")

    # CTA dopasowane do kategorii
    cta_map = {
        "payslip": "Możemy sprawdzić Twój payslip za darmo — wyślij zdjęcie w wiadomości prywatnej.",
        "umowa": "Możemy przeanalizować Twoją umowę i wskazać błędy — wyślij ją w wiadomości.",
        "bsn": "Możemy pomóc Ci przejść proces BSN krok po kroku.",
        "snf": "Możemy sprawdzić, czy potrącenia za mieszkanie są zgodne z SNF.",
        "mieszkanie": "Możemy sprawdzić Twoją umowę najmu i policzyć prawidłowe koszty.",
        "praca": "Możemy doradzić, jak rozwiązać problem z pracodawcą lub agencją.",
        "transport": "Możemy pomóc ustalić, jakie masz prawa w kwestii transportu.",
        "scam": "Uważaj — to może być oszustwo. Możemy sprawdzić tę ofertę.",
        "dramat": "Rozumiem, że sytuacja jest stresująca. Możemy pomóc to uporządkować.",
        "ogólne": "Chętnie pomożemy — napisz więcej szczegółów.",
        "spam": "Ten post wygląda na nieistotny — nie odpowiadamy."
    }

    cta = cta_map.get(category, "Chętnie pomożemy — napisz więcej szczegółów.")

    prompt = f"""
Jesteś konsultantem Polonia Assist. Odpowiadasz profesjonalnie, empatycznie i konkretnie.

Twoje zadanie:
- odpowiedzieć na post użytkownika
- dopasować ton do emocji (ton: {tone})
- uwzględnić intencję (intencja: {intent})
- uwzględnić kategorię (kategoria: {category})
- zakończyć odpowiedź CTA: "{cta}"

Treść posta:
{text}

Napisz krótką, konkretną odpowiedź (2–4 zdania).
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message["content"]
