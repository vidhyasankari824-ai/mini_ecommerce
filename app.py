from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import sqlite3
client = MongoClient("mongodb+srv://vidhya:vidhya1234@cluster0.v8q8xim.mongodb.net/?appName=Cluster0")
db = client["mini_ecommerce"]
cart_collection = db["cart"]
app = Flask(__name__)
app = Flask(__name__)
app.secret_key = "mini_ecommerce_secret"


def init_db():
    conn = sqlite3.connect("cart.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            name TEXT,
            price INTEGER
        )
    """)

    conn.commit()
    conn.close()

init_db()
app.secret_key = "mini_ecommerce_secret"

@app.route("/")
def home():
    query = request.args.get("q")

    products = [
        {
            "id": 1,
            "name": "Phone",
            "price": 12000,
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"
        },
        {
            "id": 2,
            "name": "Shoes",
            "price": 2000,
            "image": "https://images.unsplash.com/photo-1520256862855-398228c41684"
        },
        {
            "id": 3,
            "name": "Watch",
            "price": 1500,
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
        },
        {
            "id": 4,
            "name": "Headphones",
            "price": 999,
            "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
        }
    ]

    if query:
        products = [p for p in products if query.lower() in p["name"].lower()]

    cart_count = cart_collection.count_documents({})

    return render_template(
      "index.html",
      products=products,
      cart_count=cart_count
    )

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/cart")
def cart():

    items = list(cart_collection.find())

    total = sum(item["price"] for item in items)

    return render_template("cart.html", items=items, total=total)

@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/order_history")
def order_history():
    return render_template("order_history.html")


@app.route("/profile")
def profile():
    user = {
        "name": "Vidhya",
        "email": "vidhya@example.com"
    }
    return render_template("profile.html", user=user)


@app.route("/logout")
def logout():
    return "Logged out successfully"

@app.route("/cart/add/<int:id>")
def add_to_cart(id):

    products = {
        1: ("Phone", 12000),
        2: ("Shoes", 2000),
        3: ("Watch", 1500),
        4: ("Headphones", 999)
    }

    name, price = products[id]

    cart_collection.insert_one({
        "product_id": id,
        "name": name,
        "price": price
    })

    return redirect(url_for("home"))

@app.route("/cart/remove/<int:id>")
def remove_from_cart(id):

    cart_collection.delete_one({"product_id": id})

    return redirect(url_for("cart"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)