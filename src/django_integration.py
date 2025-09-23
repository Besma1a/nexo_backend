import pandas as pd


def qs_menuitems_to_df(qs) -> pd.DataFrame:
    rows = []
    for mi in qs:
        rows.append({
            "item_id": mi.pk,
            "name": mi.name,
            "category": mi.category,
            "subcategory": getattr(mi, "subcategory", None),
            "price": float(mi.price),
            "dietary_tags": getattr(mi, "dietary_tags", []) or [],
            "time_preference": getattr(mi, "time_preference", None),
            "budget_category": getattr(mi, "budget_category", None),
            "popularity_score": getattr(mi, "popularity_score", 0.0),
        })
    df = pd.DataFrame(rows)
    if "dietary_tags" in df.columns:
        df["dietary_tags"] = df["dietary_tags"].apply(lambda x: x if isinstance(x, list) else [])
    return df


def qs_orders_to_df(qs) -> pd.DataFrame:
    rows = []
    for o in qs:
        ts = getattr(o, "created_at", None) or getattr(o, "timestamp", None)
        for it in getattr(o, "items", []) or []:
            rows.append({
                "order_id": o.pk,
                "user_id": o.user_id,
                "item_id": it.get("itemId") or it.get("item_id"),
                "timestamp": ts,
            })
    return pd.DataFrame(rows)


def qs_users_to_df(qs) -> pd.DataFrame:
    rows = []
    for u in qs:
        rows.append({
            "user_id": u.pk,
            "diet": getattr(u, "diet", "none"),
            "budget_sensitivity": getattr(u, "budget_sensitivity", "medium"),
            "favorite_categories": getattr(u, "favorite_categories", []) or [],
            "time_preferences": getattr(u, "time_preferences", []) or [],
        })
    return pd.DataFrame(rows)



