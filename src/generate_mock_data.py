
import pandas as pd
import random
from datetime import datetime, timedelta

# Generate users with realistic restaurant customer data
user_data = []
names = ["Sarah Johnson", "Ahmed Benali", "Fatima Zahra", "Omar Cherif", "Emma Wilson", 
         "Carlos Rodriguez", "Priya Patel", "David Kim", "Lisa Chen", "Michael Brown",
         "Anna Schmidt", "James Taylor", "Maria Garcia", "John Smith", "Jennifer Lee",
         "Robert Davis", "Amanda White", "Christopher Jones", "Jessica Miller", "Daniel Wilson"]

for i in range(20):
    user_data.append({
        "user_id": i + 1,
        "name": names[i],
        "age": random.randint(18, 65),
        "gender": random.choice(["male", "female"]),
        "diet": random.choice(["vegetarian", "vegan", "chicken", "none"]),
        "allergies": random.choice(["", "nuts", "dairy", "eggs", "shellfish", "nuts,dairy"]),
        "budget_sensitivity": random.choice(["low", "mid", "high"]),
        "favorite_categories": random.choice(["pizza,burger", "salad,healthy", "dessert", "pasta,italian", "seafood"]),
        "disliked_categories": random.choice(["", "spicy", "seafood", "dessert"]),
        "time_preferences": random.choice(["morning,lunch", "lunch,dinner", "dinner", "morning"]),
        "spice_tolerance": random.choice(["low", "medium", "high"]),
        "health_conscious": random.choice([True, False]),
        "location": random.choice(["downtown", "suburbs", "university", "business district"]),
        "registration_date": "2023-01-01",
        "last_visit": "2024-01-15",
        "visit_frequency": random.choice(["daily", "weekly", "monthly"]),
        "avg_order_value": round(random.uniform(15, 50), 2),
        "loyalty_tier": random.choice(["bronze", "silver", "gold", "platinum"]),
        "preferred_payment": random.choice(["card", "cash", "mobile"]),
        "special_occasions": random.choice(["birthday", "anniversary", "business", "none"])
    })

users = pd.DataFrame(user_data)

# Generate items with proper restaurant data
restaurant_items = [
    {"name": "Margherita Pizza", "category": "pizza", "subcategory": "classic", "price": 15.99, "dietary_tags": "vegetarian", "time_preference": "dinner", "budget_category": "mid"},
    {"name": "Pepperoni Pizza", "category": "pizza", "subcategory": "meat", "price": 17.99, "dietary_tags": "meat", "time_preference": "dinner", "budget_category": "mid"},
    {"name": "Caesar Salad", "category": "salad", "subcategory": "classic", "price": 12.99, "dietary_tags": "vegetarian", "time_preference": "lunch", "budget_category": "mid"},
    {"name": "Grilled Chicken Salad", "category": "salad", "subcategory": "protein", "price": 14.99, "dietary_tags": "chicken", "time_preference": "lunch", "budget_category": "mid"},
    {"name": "Classic Burger", "category": "burger", "subcategory": "beef", "price": 13.99, "dietary_tags": "meat", "time_preference": "lunch", "budget_category": "mid"},
    {"name": "Veggie Burger", "category": "burger", "subcategory": "vegetarian", "price": 12.99, "dietary_tags": "vegetarian", "time_preference": "lunch", "budget_category": "mid"},
    {"name": "Chocolate Cake", "category": "dessert", "subcategory": "chocolate", "price": 8.99, "dietary_tags": "vegetarian,sweet", "time_preference": "dinner", "budget_category": "low"},
    {"name": "Tiramisu", "category": "dessert", "subcategory": "italian", "price": 9.99, "dietary_tags": "vegetarian,sweet", "time_preference": "dinner", "budget_category": "mid"},
    {"name": "Pasta Carbonara", "category": "pasta", "subcategory": "italian", "price": 16.99, "dietary_tags": "meat", "time_preference": "dinner", "budget_category": "high"},
    {"name": "Veggie Pasta", "category": "pasta", "subcategory": "vegetarian", "price": 14.99, "dietary_tags": "vegetarian", "time_preference": "dinner", "budget_category": "mid"},
    {"name": "Fish & Chips", "category": "seafood", "subcategory": "fried", "price": 18.99, "dietary_tags": "seafood", "time_preference": "dinner", "budget_category": "high"},
    {"name": "Grilled Salmon", "category": "seafood", "subcategory": "grilled", "price": 22.99, "dietary_tags": "seafood", "time_preference": "dinner", "budget_category": "high"},
    {"name": "Chicken Wings", "category": "appetizer", "subcategory": "spicy", "price": 11.99, "dietary_tags": "chicken", "time_preference": "dinner", "budget_category": "mid"},
    {"name": "Mozzarella Sticks", "category": "appetizer", "subcategory": "cheese", "price": 9.99, "dietary_tags": "vegetarian", "time_preference": "dinner", "budget_category": "low"},
    {"name": "Fresh Juice", "category": "beverage", "subcategory": "healthy", "price": 6.99, "dietary_tags": "vegetarian,healthy", "time_preference": "morning", "budget_category": "low"},
    {"name": "Coffee", "category": "beverage", "subcategory": "hot", "price": 3.99, "dietary_tags": "vegetarian", "time_preference": "morning", "budget_category": "low"},
    {"name": "Smoothie Bowl", "category": "breakfast", "subcategory": "healthy", "price": 10.99, "dietary_tags": "vegetarian,healthy", "time_preference": "morning", "budget_category": "mid"},
    {"name": "Pancakes", "category": "breakfast", "subcategory": "sweet", "price": 8.99, "dietary_tags": "vegetarian", "time_preference": "morning", "budget_category": "low"},
    {"name": "Steak", "category": "meat", "subcategory": "grilled", "price": 28.99, "dietary_tags": "meat", "time_preference": "dinner", "budget_category": "high"},
    {"name": "Veggie Wrap", "category": "wrap", "subcategory": "healthy", "price": 9.99, "dietary_tags": "vegetarian,healthy", "time_preference": "lunch", "budget_category": "low"}
]

items = pd.DataFrame(restaurant_items)
items['item_id'] = range(1, len(items) + 1)
items['description'] = items['name'] + " - Delicious " + items['category']
items['calories'] = [random.randint(200, 800) for _ in range(len(items))]
items['preparation_time'] = [random.randint(5, 25) for _ in range(len(items))]
items['popularity_score'] = [round(random.uniform(0.3, 0.9), 2) for _ in range(len(items))]
items['seasonal'] = [random.choice(['all', 'spring', 'summer', 'autumn', 'winter']) for _ in range(len(items))]
items['image_url'] = [f"images/{items.iloc[i]['category']}/{items.iloc[i]['name'].lower().replace(' ', '_')}.jpg" for i in range(len(items))]

# Generate orders
orders = []
order_items = []
order_id = 1

for _ in range(100):
    # Generate an order with multiple items
    num_items = random.randint(1, 4)  # Each order has 1-4 items
    user_id = random.choice(users["user_id"])
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
    
    for _ in range(num_items):
        item_id = random.choice(items["item_id"])
        item_info = items[items["item_id"] == item_id].iloc[0]
        
        # Generate random modifications
        added_ingredients = random.sample(["cheese", "mushrooms", "onions", "olives", "peppers"], 
                                       k=random.randint(0, 2))
        removed_ingredients = random.sample(["cheese", "mushrooms", "onions", "olives", "peppers"], 
                                         k=random.randint(0, 2))
        
        order_items.append({
            "order_id": order_id,
            "item_id": item_id,
            "quantity": random.randint(1, 3),
            "price": item_info["price"],
            "added_ingredients": ",".join(added_ingredients) if added_ingredients else "",
            "removed_ingredients": ",".join(removed_ingredients) if removed_ingredients else ""
        })
    
    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "total_amount": sum(item["price"] * item["quantity"] for item in order_items[-num_items:])
    })
    order_id += 1

orders = pd.DataFrame(orders)
order_items = pd.DataFrame(order_items)

# Saving 
users.to_csv("data/raw/users.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
orders.to_csv("data/raw/orders.csv", index=False)
order_items.to_csv("data/raw/order_items.csv", index=False)

print("✅ Mock data generated in data/raw/")
