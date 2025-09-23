from __future__ import annotations

import math
import pandas as pd
from typing import List, Dict
from .data_loader import load_all
from .contextual import Context
from .collaborative import cf_scores_for_user


def compute_user_favorites(orders: pd.DataFrame) -> pd.Series:
    return orders.groupby(["user_id", "item_id"]).size().groupby(level=0).apply(
        lambda s: (s - s.min()) / (s.max() - s.min() + 1e-6)
    )


def score_items(user_id: int, ctx: Context, users: pd.DataFrame, items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    ctx.ensure()

    # Base score by item popularity
    popularity = orders.groupby("item_id").size()
    popularity = (popularity - popularity.min()) / (popularity.max() - popularity.min() + 1e-6)

    df = items.copy()
    df["base"] = df["item_id"].map(popularity).fillna(0.2)

    # Diet filter/boost
    user = users.loc[users.user_id == user_id].iloc[0]
    diet = str(user.get("diet", "none"))
    def diet_ok(tags: List[str]) -> float:
        tags = set(tags or [])
        if diet == "vegetarian" and "meat" in tags:
            return 0.0
        if diet == "vegan" and any(t in tags for t in ["meat", "vegetarian", "dairy", "cheese"]):
            return 0.0
        if diet == "chicken" and "meat" in tags and "chicken" not in tags:
            return 0.5
        return 1.0

    df["diet_multiplier"] = df["dietary_tags"].apply(diet_ok)

    # Time-of-day boosts
    df["time_multiplier"] = (df["time_preference"].fillna("any").apply(
        lambda t: 1.2 if t == ctx.time_of_day else (1.05 if t in ["any", "all"] else 1.0)
    ))

    # Budget sensitivity
    budget = ctx.budget_level or (str(user.get("budget_sensitivity", "medium")))
    def budget_mult(cat: str) -> float:
        if budget in ["low", "high", "mid", "medium"]:
            mapping = {
                "low": {"low": 1.2, "mid": 1.0, "high": 0.8},
                "medium": {"low": 1.1, "mid": 1.1, "high": 0.95},
                "mid": {"low": 1.1, "mid": 1.1, "high": 0.95},
                "high": {"low": 0.9, "mid": 1.0, "high": 1.2},
            }
            return mapping["medium" if budget == "mid" else budget].get(cat, 1.0)
        return 1.0
    df["budget_multiplier"] = df["budget_category"].fillna("mid").apply(budget_mult)

    # User favorites from orders
    fav_series = compute_user_favorites(orders).get(user_id, pd.Series(dtype=float))
    fav_map = fav_series if isinstance(fav_series, pd.Series) else pd.Series(dtype=float)
    df["favorite_boost"] = df["item_id"].map(fav_map).fillna(0.0) * 0.6 + 1.0

    # Final score
    df["score"] = df["base"] * df["diet_multiplier"] * df["time_multiplier"] * df["budget_multiplier"] * df["favorite_boost"]
    return df.sort_values("score", ascending=False)


def recommend(user_id: int, top_k: int = 10, ctx: Context | None = None) -> pd.DataFrame:
    users, items, orders = load_all()
    ctx = ctx or Context(user_id=user_id, now=pd.Timestamp.now()).ensure()
    content_scored = score_items(user_id, ctx, users, items, orders)

    # Collaborative filtering scores
    cf = cf_scores_for_user(user_id)
    if not cf.empty:
        # Normalize CF to 0..1
        cf_norm = (cf - cf.min()) / (cf.max() - cf.min() + 1e-6)
        content_scored["cf_score"] = content_scored["item_id"].map(cf_norm).fillna(0.0)
    else:
        content_scored["cf_score"] = 0.0

    # Hybrid combine: weighted geometric mean (robust to scale), with content/context dominant
    content_scored["hybrid_score"] = (
        (content_scored["score"] + 1e-6) ** 0.7 * (content_scored["cf_score"] + 1e-6) ** 0.3
    )
    scored = content_scored.sort_values("hybrid_score", ascending=False)
    cols = [
        "item_id", "name", "category", "subcategory", "price", "dietary_tags", "time_preference", "budget_category", "score"
    ]
    cols += ["cf_score", "hybrid_score"]
    return scored[cols].head(top_k)


