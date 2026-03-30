from groups import get_page_groups
from posts import get_recent_posts_without_pa_comment
from classifier import classify_post


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

        # 4. Wyświetl posty i klasyfikację
        for post in posts:
            print("Post:", post.get("message", "[brak treści]"))
            classification = classify_post(post.get("message", ""))
            print("Klasyfikacja:", classification)

    print("=== KONIEC CYKLU ===")


if __name__ == "__main__":
    print("=== TEST DEPLOYU ===")
    run_agent_cycle()
