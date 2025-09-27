import pandas as pd
from datetime import datetime
from typing import Tuple


def load_users(path: str = "data/raw/users.csv") -> pd.DataFrame:
    users = pd.read_csv(path)
    # Normalize list-like fields if present
    for col in [
        "favorite_categories",
        "disliked_categories",
        "time_preferences",
        "allergies",
    ]:
        if col in users.columns:
            users[col] = users[col].fillna("").apply(
                lambda x: [v.strip() for v in str(x).split(",") if v.strip()]
            )
    return users


def load_items(path: str = "data/raw/items.csv") -> pd.DataFrame:
    items = pd.read_csv(path)
    # Ensure types
    if "dietary_tags" in items.columns:
        items["dietary_tags"] = items["dietary_tags"].fillna("").apply(
            lambda x: [v.strip() for v in str(x).split(",") if v.strip()]
        )
    return items


def _infer_time_of_day(ts: datetime) -> str:
    h = ts.hour
    if 6 <= h < 11:
        return "morning"
    if 11 <= h < 15:
        return "lunch"
    if 15 <= h < 18:
        return "afternoon"
    return "dinner"


def load_orders(orders_path: str = "data/raw/orders.csv", 
                order_items_path: str = "data/raw/order_items.csv") -> pd.DataFrame:
    orders = pd.read_csv(orders_path, parse_dates=["timestamp"], dayfirst=False)
    order_items = pd.read_csv(order_items_path)
    
    # Parse list-like fields
    for col in ['added_ingredients', 'removed_ingredients']:
        if col in order_items.columns:
            order_items[col] = order_items[col].fillna("").apply(
                lambda x: [v.strip() for v in str(x).split(",") if v.strip()]
            )
    
    # Add derived fields
    if "time_of_day" not in orders.columns:
        orders["time_of_day"] = orders["timestamp"].apply(_infer_time_of_day)
    
    # Merge orders with order_items to get complete information
    complete_orders = pd.merge(orders, order_items, on="order_id", how="left")
    return complete_orders


def load_all() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return load_users(), load_items(), load_orders()





