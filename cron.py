import requests
from datetime import datetime, timedelta
from config import FB_PAGE_ID, FB_PAGE_TOKEN


def get_recent_posts_without_pa_comment():
    """
    Pobiera posty z FEEDU STRONY (FB_PAGE_ID):
    - nie starsze niż 12 godzin
    - bez komentarza Polonia Assist
    - mogą pochodzić z grup, w których strona jest członkiem
    """

    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/feed"
    params = {
        "access_token": FB_PAGE_TOKEN,
        "limit": 50,
        "fields": "id,message,created_time,permalink_url,from"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "data" not in data:
        print("Brak danych z feedu strony:", data)
        return []

    now = datetime.utcnow()
    cutoff = now - timedelta(hours=12)

    valid_posts = []

    for post in data["data"]:
        created_raw = post.get("created_time")
        if not created_raw:
            continue

        try:
            created = datetime.strptime(created_raw, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        except Exception:
            continue

        if created < cutoff:
            continue

        # sprawdź, czy już komentowaliśmy ten post jako strona
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

        if already_commented:
            continue

        valid_posts.append(post)

    return valid_posts


def send_comment(post_id, message):
    """
    Wysyła komentarz jako strona Polonia Assist NL.
    """
    url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
    payload = {
        "message": message,
        "access_token": FB_PAGE_TOKEN
    }

    response = requests.post(url, data=payload)
    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    return data

