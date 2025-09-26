import pandas as pd
import numpy as np
from .data_loader import load_orders


class PopularityRecommender:
    """Popularity-based recommendation system"""

    def __init__(self, orders, order_items):
        self.orders = orders
        self.order_items = order_items
        self._calculate_popularity()

    def _calculate_popularity(self):
        """Calculate item popularity scores"""
        # Merge orders with items
        merged = pd.merge(
            self.orders,
            self.order_items,
            on="order_id",
        )

        # Calculate popularity scores
        self.popularity_scores = merged.groupby("item_id")["quantity"].sum()

        # Normalize scores
        self.popularity_scores = self.popularity_scores / self.popularity_scores.max()

    def recommend(self, user_id, k=5):
        """Get top-k popular items"""
        try:
            # Return top-k popular items
            return self.popularity_scores.nlargest(k)
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return pd.Series()

def item_popularity() -> pd.Series:
    orders = load_orders()
    return orders.groupby("item_id").size().sort_values(ascending=False)




