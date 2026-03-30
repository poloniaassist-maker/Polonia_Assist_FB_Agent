from groups import get_page_groups
from posts import get_recent_posts_without_pa_comment

def run_agent_cycle():
    print("=== START AGENTA POLONIA ASSIST ===")

    # 1. Pobierz wszystkie grupy strony
    groups = get_page_groups()
    print("Znalezione grupy:", groups)

    # 2. Pobierz posty z każdej grupy
    for group in groups:
        print(f"\n--- Grupa: {group['name']} ---")
        posts = get_recent_posts_without_pa_comment(group["id"])
        print(f"Posty do obsługi: {len(posts)}")

        for post in posts:
            print("Post:", post.get("message", "[brak treści]"))
            # tutaj później dodamy Moduł 4, 5 i 6

    print("=== KONIEC CYKLU ===")

if __name__ == "__main__":
    run_agent_cycle()
