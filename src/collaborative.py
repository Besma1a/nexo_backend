from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Tuple
from .data_loader import load_orders


def user_item_matrix() -> pd.DataFrame:
    orders = load_orders()
    mat = orders.pivot_table(
        index="user_id",
        columns="item_id",
        values="order_id",
        aggfunc="count",
        fill_value=0,
    ).astype(float)
    return mat


def _cosine_similarity(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=0, keepdims=True) + 1e-9
    normalized = matrix / norms
    return normalized.T @ normalized


def item_similarity(mat: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Index, pd.Index]:
    sim = _cosine_similarity(mat.values)
    return pd.DataFrame(sim, index=mat.columns, columns=mat.columns), mat.index, mat.columns


def cf_scores_for_user(user_id: int, top_k: int | None = None) -> pd.Series:
    mat = user_item_matrix()
    if user_id not in mat.index:
        return pd.Series(dtype=float)

    sim, _, items = item_similarity(mat)

    user_vector = mat.loc[user_id]
    # Predicted preference for each item = weighted sum of similarities to items the user interacted with
    weights = user_vector.values
    if np.all(weights == 0):
        return pd.Series(dtype=float)

    scores = sim.values @ weights
    scores = pd.Series(scores, index=items)
    # Do not recommend items already consumed heavily; demote those
    scores -= user_vector * 0.5
    scores = scores.clip(lower=0)

    if top_k:
        scores = scores.nlargest(top_k)
    return scores



