from flask import Flask, render_template, redirect, url_for, session, request
print("APP.PY IS RUNNING")
from dotenv import load_dotenv
from pymongo import MongoClient
import os
from bson.objectid import ObjectId


app = Flask(__name__)
@app.route("/")
def home():
    return "App is working!"
app.secret_key = "vidhya123"

load_dotenv()

print("MONGO_URI =", os.getenv("MONGO_URI"))

client = MongoClient(os.getenv("MONGO_URI"))

db = client["ecommerce"]

users = db["users"]
admins = db["admins"]
products_collection = db["products"]
orders = db["orders"]

# Home Page
@app.route("/")
def home():
    products = list(products_collection.find())
    return render_template("index.html", products=products)

# User Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })

        return redirect(url_for("login"))

    return render_template("register.html")

# User Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = users.find_one({
            "email": email,
            "password": password
        })

        if user:
            session["user"] = str(user["_id"])
            return redirect(url_for("home"))

        return "Invalid Email or Password"
    return render_template("login.html")
# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Order History
@app.route("/order_history")
def order_history():

    all_orders = list(orders.find())

    return render_template(
        "order_history.html",
        orders=all_orders
    )

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect(url_for("login"))

    user = users.find_one({"_id": ObjectId(session["user"])})

    return render_template("profile.html", user=user)

# Add to Cart
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):

    cart = session.get("cart", [])
    cart.append(id)
    session["cart"] = cart

    return redirect(url_for("home"))


# View Cart
@app.route("/cart")
def cart():

    cart = session.get("cart", [])
    cart_products = []
    total = 0

    for item in cart:
        product = products_collection.find_one({"id": item})

        if product:
            cart_products.append(product)
            total += product["price"]

    return render_template(
        "cart.html",
        cart_products=cart_products,
        total=total
    )


# Remove from Cart
@app.route("/remove_from_cart/<int:id>")
def remove_from_cart(id):

    cart = session.get("cart", [])

    if id in cart:
        cart.remove(id)

    session["cart"] = cart

    return redirect(url_for("cart"))


# Checkout
@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


# Place Order
@app.route("/place_order", methods=["POST"])
def place_order():

    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]

    cart = session.get("cart", [])

    cart_products = []
    total = 0

    for item in cart:

        product = products_collection.find_one({"id": item})

        if product:
            cart_products.append(product)
            total += product["price"]

    orders.insert_one({
        "name": name,
        "phone": phone,
        "address": address,
        "products": cart_products,
        "total": total,
        "status": "Pending"
    })

    session["cart"] = []

    return redirect(url_for("home"))
# Admin Login
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = admins.find_one({
            "username": username,
            "password": password
        })

        if admin:
            return redirect(url_for("admin_dashboard"))

        return "Invalid Admin Login"

    return render_template("admin_login.html")
# Add Product
@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        product_count = products_collection.count_documents({}) + 1

        products_collection.insert_one({
            "id": product_count,
            "name": request.form["name"],
            "price": int(request.form["price"]),
            "image": request.form["image"],
            "stock": int(request.form["stock"])
        })

        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")

@app.route("/approve_order/<order_id>")
def approve_order(order_id):

    orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "Approved"}}
    )

    return redirect(url_for("admin_dashboard"))

# Admin Dashboard
@app.route("/admin_dashboard")
def admin_dashboard():

    all_users = list(users.find())
    all_products = list(products_collection.find())
    all_orders = list(orders.find())

    return render_template(
        "admin_dashboard.html",
        users=all_users,
        products=all_products,
        orders=all_orders
    )


if __name__ == "__main__":
    app.run(debug=False)

    if __name__ == "__main__":
      app.run(host="0.0.0.0", port=10000)