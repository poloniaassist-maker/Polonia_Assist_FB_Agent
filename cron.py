from posts import get_recent_posts_without_pa_comment, send_comment
from classifier import classify_post
from generate_reply import generate_reply
from anti_duplicate import already_replied, mark_as_replied, is_old_post


def run_agent_cycle():
    print("=== START AGENTA POLONIA ASSIST (FEED STRONY) ===")

    posts = get_recent_posts_without_pa_comment()
    print(f"Posty do obsługi: {len(posts)}")

    for post in posts:
        message = post.get("message", "")
        post_id = post.get("id")
        permalink = post.get("permalink_url", "")

        print("\n--- POST ---")
        print("ID:", post_id)
        print("Link:", permalink)
        print("Treść:", message or "[brak treści]")

        if not post_id:
            print("Brak ID posta — pomijam.")
            continue

        if already_replied(post_id):
            print("Pomijam — już odpowiadaliśmy na ten post (anti_duplicate).")
            continue

        if is_old_post(post):
            print("Pomijam — post starszy niż dopuszczalny limit.")
            continue

        classification = classify_post(message)
        print("Klasyfikacja:", classification)

        if not classification.get("should_reply", True):
            print("Pomijam — should_reply = false")
            continue

        reply = generate_reply(classification, message)
        print("Odpowiedź:", reply)

        try:
            send_comment(post_id, reply)
            print("Komentarz wysłany.")
            mark_as_replied(post_id)
        except Exception as e:
            print("Błąd przy wysyłaniu komentarza:", e)

    print("=== KONIEC CYKLU ===")
