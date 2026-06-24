from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

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
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)