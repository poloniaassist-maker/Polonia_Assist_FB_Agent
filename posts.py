import requests
import os
from datetime import datetime, timedelta

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")

def get_recent_posts_without_pa_comment(group_id):
    """
    Pobiera posty z grupy:
    - nie starsze niż 12 godzin
    - bez komentarza Polonia Assist
    """

    # 1. Pobierz feed grupy
    url = f"https://graph.facebook.com/v18.0/{group_id}/feed"
    params = {
        "access_token": FB_PAGE_TOKEN,
        "limit": 25,  # wystarczy do 12h
        "fields": "id,message,created_time"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "data" not in data:
        return []

    now = datetime.utcnow()
    cutoff = now - timedelta(hours=12)

    valid_posts = []

    for post in data["data"]:
        # --- 2. Filtr: post nie starszy niż 12 godzin ---
        created = datetime.strptime(
            post["created_time"], "%Y-%m-%dT%H:%M:%S%z"
        ).replace(tzinfo=None)

        if created < cutoff:
            continue

        # --- 3. Filtr: brak komentarza Polonia Assist ---
        comments_url = f"https://graph.facebook.com/v18.0/{post['id']}/comments"
        comments_params = {
            "access_token": FB_PAGE_TOKEN,
            "filter": "stream",
            "fields": "from"
        }

        comments_res = requests.get(comments_url, params=comments_params).json()

        already_commented = False

        if "data" in comments_res:
            for c in comments_res["data"]:
                if c.get("from", {}).get("id") == FB_PAGE_ID:
                    already_commented = True
                    break

        if not already_commented:
            valid_posts.append(post)

    return valid_posts
def send_comment(post_id, message):
    """
    Wysyła komentarz jako strona Polonia Assist.
    """
    url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
    params = {
        "access_token": FB_PAGE_TOKEN,
        "message": message,
    }

    response = requests.post(url, params=params)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid JSON response", "status_code": response.status_code, "text": response.text}
