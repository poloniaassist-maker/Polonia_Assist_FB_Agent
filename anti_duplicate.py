import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "reply_cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {"replied_posts": []}
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"replied_posts": []}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def already_replied(post_id: str) -> bool:
    cache = load_cache()
    return post_id in cache["replied_posts"]


def mark_as_replied(post_id: str):
    cache = load_cache()
    if post_id not in cache["replied_posts"]:
        cache["replied_posts"].append(post_id)
        save_cache(cache)


def is_old_post(post) -> bool:
    """
    Filtr: nie odpowiadamy na posty starsze niż 48h.
    """
    created = post.get("created_time")
    if not created:
        return False

    try:
        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        return created_dt < datetime.utcnow() - timedelta(hours=48)
    except:
        return False
