
import pandas as pd
import random
from datetime import datetime, timedelta

# Generate users
users = pd.DataFrame({
    "user_id": range(1, 21),
    "name": [f"User{i}" for i in range(1, 21)],
    "diet": [random.choice(["vegetarian", "vegan", "chicken", "none"]) for _ in range(20)]
})

# Generate items
items = pd.DataFrame({
    "item_id": range(1, 11),
    "name": [f"Dish{i}" for i in range(1, 11)],
    "category": [random.choice(["pizza", "burger", "salad", "dessert"]) for _ in range(10)],
    "price": [round(random.uniform(5, 20), 2) for _ in range(10)]
})

# Generate orders
orders = []
for _ in range(100):
    orders.append({
        "order_id": random.randint(1, 1000),
        "user_id": random.choice(users["user_id"]),
        "item_id": random.choice(items["item_id"]),
        "timestamp": datetime.now() - timedelta(days=random.randint(0, 30))
    })
orders = pd.DataFrame(orders)

# Saving 
users.to_csv("data/raw/users.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
orders.to_csv("data/raw/orders.csv", index=False)

print("✅ Mock data generated in data/raw/")
