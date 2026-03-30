import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_post(text):
    """
    Klasyfikuje post:
    - czy to pytanie
    - czy dotyczy Holandii
    - czy pasuje do działalności Polonia Assist
    """

    prompt = f"""
    Przeanalizuj poniższy post z Facebooka i odpowiedz w JSON.

    Post:
    \"\"\"{text}\"\"\"

    Oceń:
    1. is_question — czy post zawiera pytanie (true/false)
    2. is_about_netherlands — czy dotyczy życia lub pracy w Holandii (true/false)
    3. is_relevant_to_polonia_assist — czy temat pasuje do działalności Polonia Assist NL:
       - praca, prawa pracownika, umowy
       - BSN, DigiD, meldunek
       - ubezpieczenia, zorgtoeslag
       - podatki, rozliczenia
       - mieszkania, SNF
       - mandaty, transport
       - życie codzienne w NL

    Zwróć TYLKO JSON, bez komentarza.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
