import pandas as pd
from .data_loader import load_orders


def item_popularity() -> pd.Series:
    orders = load_orders()
    return orders.groupby("item_id").size().sort_values(ascending=False)



