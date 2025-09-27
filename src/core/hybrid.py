from __future__ import annotations

import math
import pandas as pd
from typing import List, Dict
from .data_loader import load_all
from .contextual import Context
from .collaborative import cf_scores_for_user
from .utils import season_of


def compute_user_favorites(orders: pd.DataFrame) -> pd.Series:
    return orders.groupby(["user_id", "item_id"]).size().groupby(level=0).apply(
        lambda s: (s - s.min()) / (s.max() - s.min() + 1e-6)
    )


def score_items(user_id: int, ctx: Context, users: pd.DataFrame, items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    ctx.ensure()

    # Base score: recency-decayed popularity
    now = pd.Timestamp.now()
    orders = orders.assign(_age_days=(now - orders["timestamp"]).dt.days.clip(lower=0))
    decay = 0.5 ** (orders["_age_days"] / 30.0)  # half-life ~30 days
    popularity = orders.groupby("item_id").apply(lambda g: (0.2 + decay.loc[g.index]).sum())
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

    # Seasonality boost (items seasonal == current season)
    current_season = season_of(ctx.now)
    if "seasonal" in df.columns:
        df["season_multiplier"] = df["seasonal"].fillna("all").apply(
            lambda s: 1.15 if s == current_season or s in ["all", "any"] else 1.0
        )
    else:
        df["season_multiplier"] = 1.0

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

    # Price alignment to user's historical spend (optional gentle pull)
    user_spend = orders.loc[orders.user_id == user_id]
    if not user_spend.empty and "price" in df.columns and "item_id" in user_spend.columns:
        # approximate average ticket from orders if total_amount exists; else skip
        # here we softly center around user's avg item price inferred from items ordered
        joined = user_spend.merge(df[["item_id", "price"]], on="item_id", how="left")
        # Use price_y (from items) or price_x (from orders) depending on what's available
        price_col = "price_y" if "price_y" in joined.columns else "price_x" if "price_x" in joined.columns else "price"
        if price_col in joined.columns:
            target = joined[price_col].dropna().mean()
        else:
            target = user_spend["total_amount"].mean() / 2  # Fallback
        if pd.notna(target):
            df["price_align"] = (1.0 - (df["price"] - target).abs() / (target + 1e-6)).clip(0.8, 1.2)
        else:
            df["price_align"] = 1.0
    else:
        df["price_align"] = 1.0

    # Recent-purchase penalty: avoid recommending the exact same item immediately
    recent = orders.sort_values("timestamp").groupby("user_id").tail(3)
    recent_ids = set(recent.loc[recent.user_id == user_id, "item_id"].tolist())
    df["recent_penalty"] = df["item_id"].apply(lambda x: 0.85 if x in recent_ids else 1.0)

    # Final score (content/context)
    df["score"] = (
        df["base"]
        * df["diet_multiplier"]
        * df["time_multiplier"]
        * df["season_multiplier"]
        * df["budget_multiplier"]
        * df["favorite_boost"]
        * df["price_align"]
        * df["recent_penalty"]
    )
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

    # Simple diversity re-ranking: limit top-N per category
    max_per_category = 3
    seen = {}
    diversified = []
    for _, row in scored.iterrows():
        cat = row.get("category")
        count = seen.get(cat, 0)
        if count < max_per_category:
            diversified.append(row)
            seen[cat] = count + 1
        if len(diversified) >= 100:
            break
    scored = pd.DataFrame(diversified) if diversified else scored
    cols = [
        "item_id", "name", "category", "subcategory", "price", "dietary_tags", "time_preference", "budget_category", "score"
    ]
    cols += ["cf_score", "hybrid_score"]
    return scored[cols].head(top_k)


