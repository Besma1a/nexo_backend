from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Tuple
from pathlib import Path
from .data_loader import load_orders  # Update import to use relative path
from .collaborative import user_item_matrix, item_similarity, cf_scores_for_user


def user_item_matrix() -> pd.DataFrame:
    orders = load_orders()
    mat = orders.pivot_table(
        index="user_id",
        columns="item_id",
        values="quantity",
        aggfunc="sum",  # If a user orders the same item multiple times 
        fill_value=0,
    ).astype(float)
    
    # Add weight for customizations (added/removed ingredients)
    customization_weight = 0.2  # Adjust this value based on how much you want to emphasize modifications
    
    for user_id in mat.index:
        user_orders = orders[orders["user_id"] == user_id]
        for item_id in mat.columns:
            item_orders = user_orders[user_orders["item_id"] == item_id]
            if not item_orders.empty:
                # Count number of modifications
                modifications = sum(
                    len(mods) if isinstance(mods, list) else 0
                    for mods in item_orders["added_ingredients"].tolist() + 
                    item_orders["removed_ingredients"].tolist()
                )
                # Add weighted modification score to the interaction strength
                mat.loc[user_id, item_id] += modifications * customization_weight
    
    return mat


def _cosine_similarity(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=0, keepdims=True) + 1e-9 # Prevent division by zero
    normalized = matrix / norms
    return normalized.T @ normalized

#how similar each food item is to every other food
def item_similarity(mat: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Index, pd.Index]:
    sim = _cosine_similarity(mat.values)
    return pd.DataFrame(sim, index=mat.columns, columns=mat.columns), mat.index, mat.columns


def cf_scores_for_user(user_id: int, top_k: int | None = None) -> pd.Series:
    mat = user_item_matrix()
    if user_id not in mat.index:
        return pd.Series(dtype=float)

    sim, _, items = item_similarity(mat)

    user_vector = mat.loc[user_id]
    weights = user_vector.values
    if np.all(weights == 0):
        return pd.Series(dtype=float)

    scores = sim.values @ weights
    scores = pd.Series(scores, index=items)
    # Do not recommend items already consumed heavily
    scores -= user_vector * 0.5
    scores = scores.clip(lower=0) #remove negative 

    if top_k:
        scores = scores.nlargest(top_k)
    return scores


class CollaborativeFiltering:
    """Wrapper class for collaborative filtering functions"""
    
    def __init__(self, orders, order_items):
        self.orders = orders
        self.order_items = order_items
        self.matrix = user_item_matrix()
        self.similarity_matrix, _, self.items = item_similarity(self.matrix)
    
    def recommend(self, user_id: int, k: int = 5) -> pd.Series:
        """Generate recommendations for a user"""
        try:
            # Use existing cf_scores_for_user function
            scores = cf_scores_for_user(user_id, top_k=k)
            return scores
            
        except Exception as e:
            print(f"Error generating recommendations for user {user_id}: {e}")
            return pd.Series()



