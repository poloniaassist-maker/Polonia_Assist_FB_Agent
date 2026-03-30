from groups import get_page_groups
from posts import get_recent_posts_without_pa_comment, send_comment
from classifier import classify_post
from generate_reply import generate_reply


def run_agent_cycle():
    print("=== START AGENTA POLONIA ASSIST ===")

    # 1. Pobierz wszystkie grupy
    groups = get_page_groups()
    print("Znalezione grupy:", groups)

    # 2. Przejdź przez każdą grupę
    for group in groups:
        print(f"\n--- Grupa: {group['name']} ---")

        # 3. Pobierz posty z tej grupy
        posts = get_recent_posts_without_pa_comment(group["id"])
        print(f"Posty do obsługi: {len(posts)}")

        # 4. Przetwarzaj posty: klasyfikacja + odpowiedź + komentarz
        for post in posts:
            message = post.get("message", "")
            print("Post:", message or "[brak treści]")

            # Klasyfikacja
            classification = classify_post(message)
            print("Klasyfikacja:", classification)

            # Jeśli klasyfikator mówi, że nie odpowiadamy → pomijamy
            if not classification.get("should_reply", True):
                print("Pomijam post — should_reply = false")
                continue

            # Generowanie odpowiedzi
            reply = generate_reply(classification, message)
            print("Odpowiedź:", reply)

            # Wysyłanie komentarza
            try:
                send_comment(post["id"], reply)
                print("Komentarz wysłany.")
            except Exception as e:
                print("Błąd przy wysyłaniu komentarza:", e)

    print("=== KONIEC CYKLU ===")


if __name__ == "__main__":
    print("=== TEST DEPLOYU ===")
    run_agent_cycle()
