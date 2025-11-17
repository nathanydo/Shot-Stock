from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

drinks = [
    {"name": "Vodka", "price": 1, "sales": 0},
    {"name": "Rum", "price": 1, "sales": 0},
    {"name": "Tequila", "price": 1, "sales": 0},
    {"name": "Gin", "price": 1, "sales": 0},
    {"name": "Whiskey", "price": 1, "sales": 0},
]

total_orders = 0
price_history = []  # Track price history for graphing

@app.route("/")
def index():
    return render_template("index.html", drinks=drinks)

@socketio.on("order")
def handle_order(data):
    global total_orders
    idx = int(data["drink_index"])
    drinks[idx]["sales"] += 1
    total_orders += 1

    # Example: price logic can be customized here
    if total_orders % 3 == 0:
        # if drinks[idx]["price"] < 5:
        drinks[idx]["price"] = min(5, drinks[idx]["price"] + 1)
        max_price = max(d["price"] for d in drinks)
        if max_price >= 5:
            other_indices = [i for i in range(len(drinks)) if i != idx]
            num_to_decrease = random.randint(1, len(other_indices))
            drinks_to_decrease = random.sample(other_indices, num_to_decrease)
            for i in drinks_to_decrease:
                drinks[i]["price"] = max(1, min(5, drinks[i]["price"] - 1))

    # Record current prices
    price_history.append({
        "order": total_orders,
        "prices": {d["name"]: int(round(d["price"])) for d in drinks}
    })
    # Send drinks with integer prices for display
    display_drinks = [{**d, "price": int(round(d["price"]))} for d in drinks]
    emit("update", {"drinks": display_drinks, "history": price_history}, broadcast=True)

def price_variance_task():
    while True:
        time.sleep(3)  # Change for rate of price change
        changed = False
        for d in drinks:
            bounce = random.choice([-1, 1])
            new_price = round(d["price"] + bounce, 2)
            if 1 <= new_price <= 5:
                d["price"] = new_price
                changed = True
        if changed:
            # Record current prices with a pseudo order number (fractional for time events)
            pseudo_order = total_orders + len(price_history) * 0.01
            price_history.append({
                "order": pseudo_order,
                "prices": {d["name"]: int(round(d["price"])) for d in drinks}
            })
            display_drinks = [{**d, "price": int(round(d["price"]))} for d in drinks]
            socketio.emit("update", {"drinks": display_drinks, "history": price_history})

# Start the background price variance task
def start_background_tasks():
    t = threading.Thread(target=price_variance_task, daemon=True)
    t.start()

if __name__ == "__main__":
    start_background_tasks()
    socketio.run(app, debug=True)