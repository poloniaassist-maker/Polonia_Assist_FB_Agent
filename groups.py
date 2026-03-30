import requests
import os

FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")

def get_page_groups():
    """
    Pobiera wszystkie grupy, do których należy strona Polonia Assist.
    Automatycznie uwzględnia nowe grupy.
    """
    url = f"https://graph.facebook.com/v18.0/{FB_PAGE_ID}/groups"
    params = {
        "access_token": FB_PAGE_TOKEN,
        "limit": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    groups = []

    if "data" in data:
        for g in data["data"]:
            groups.append({
                "id": g["id"],
                "name": g.get("name", "Unknown Group")
            })

    return groups
