from __future__ import annotations

import random
import pandas as pd
from datetime import datetime
from .data_loader import load_all
from .contextual import Context


def generate_notifications(user_id: int, now: datetime | None = None) -> list[dict]:
    users, items, orders = load_all()
    now = now or pd.Timestamp.now().to_pydatetime()
    ctx = Context(user_id=user_id, now=now).ensure()

    user = users.loc[users.user_id == user_id].iloc[0]
    msgs: list[dict] = []

    # Favorite item reminder
    fav_counts = orders[orders.user_id == user_id].groupby("item_id").size().sort_values(ascending=False)
    if not fav_counts.empty:
        fav_id = fav_counts.index[0]
        fav = items.loc[items.item_id == fav_id].iloc[0]
        msgs.append({
            "type": "favorite_discount",
            "title": "Your favorite is on promo!",
            "body": f"{fav['name']} is 15% off today.",
            "cta": "Order now"
        })

    # Time-of-day suggestion
    suggestions = items[items.time_preference.fillna("any").isin([ctx.time_of_day, "any", "all"])].sample(n=1, random_state=1)
    if not suggestions.empty:
        it = suggestions.iloc[0]
        msgs.append({
            "type": "time_suggestion",
            "title": "Perfect for now",
            "body": f"It's {ctx.time_of_day}! Try {it['name']}.",
            "cta": "See details"
        })

    # New item in favorite category 
    fav_cats = user.get("favorite_categories", [])
    if fav_cats:
        cat = random.choice(fav_cats)
        cand = items[items.category == cat].sort_values("popularity_score", ascending=False).head(1)
        if not cand.empty:
            it = cand.iloc[0]
            msgs.append({
                "type": "new_item",
                "title": f"New in {cat}",
                "body": f"Check out {it['name']} in {cat}.",
                "cta": "Explore"
            })

    return msgs




