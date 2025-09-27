from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np


@dataclass
class Context:
    user_id: int
    now: datetime
    budget_level: str | None = None  # low | mid | high
    time_of_day: str | None = None   # morning | lunch | afternoon | dinner

    def ensure(self):
        if not self.time_of_day:
            h = self.now.hour
            if 6 <= h < 11:
                self.time_of_day = "morning"
            elif 11 <= h < 15:
                self.time_of_day = "lunch"
            elif 15 <= h < 18:
                self.time_of_day = "afternoon"
            else:
                self.time_of_day = "dinner"
        return self


class ContextualRecommender:
    """Contextual recommendation system based on user and order context"""

    def __init__(self, orders, order_items, users):
        self.orders = orders
        self.order_items = order_items
        self.users = users
        self._prepare_data()

    def _prepare_data(self):
        """Prepare data for contextual recommendations"""
        # Merge orders with items
        self.user_items = pd.merge(
            self.orders,
            self.order_items,
            on="order_id",
        )

        # Calculate user-item interaction matrix
        self.interaction_matrix = self.user_items.pivot_table(
            index="user_id",
            columns="item_id",
            values="quantity",
            aggfunc="sum",
            fill_value=0,
        )

    def recommend(self, user_id, k=5):
        """Generate contextual recommendations for a user"""
        try:
            # Get user's history
            user_history = self.interaction_matrix.loc[user_id]

            # Calculate item scores based on context
            scores = pd.Series(
                np.zeros(len(self.interaction_matrix.columns)),
                index=self.interaction_matrix.columns,
            )

            # Simple scoring based on item popularity and user history
            for item_id in self.interaction_matrix.columns:
                if user_history[item_id] == 0:  # Only recommend unordered items
                    item_popularity = self.interaction_matrix[item_id].mean()
                    scores[item_id] = item_popularity

            # Return top-k recommendations
            return scores.nlargest(k)

        except KeyError:
            print(f"User {user_id} not found in interaction matrix")
            return pd.Series()
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return pd.Series()




