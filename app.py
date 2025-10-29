import os
import sqlite3

from flask import Flask, render_template, g, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, instance_relative_config=True)

os.makedirs(app.instance_path, exist_ok=True)
app.config["SECRET_KEY"] = "secret"

DB_PATH = os.path.join(app.instance_path, "data.db")

with app.app_context():
    db = sqlite3.connect(DB_PATH)
    with open(os.path.join(os.path.dirname(__file__), "data.sql"), "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()
    db.close()

def run_query(query, args=(), fetch=True):
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    cur = g.db.execute(query, args)
    rows = None
    if fetch:
        rows = cur.fetchall()
    else:
        g.db.commit()
    cur.close()
    return rows

@app.route("/")
def index():
    user_id = session.get("user_id")
    if user_id:
        return redirect("/home")
    return render_template("index.html")

@app.get("/about")
def get_about():
    return render_template("about.html")

@app.get("/profile")
def get_profile():
    return render_template("profile.html")


@app.get("/contact")
def get_contact():
    return render_template("contact.html")

@app.get("/signin")
def get_signin():
    return render_template("signin.html")

@app.get("/signup")
def get_signup():
    return render_template("signup.html")

@app.get("/home")
def get_home():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    accounts= run_query("SELECT * FROM bank_accounts WHERE user_id = ?", (user_id,))
    return render_template("home.html", bank_accounts=accounts)

@app.post("/signin")
def post_signin():
    email = request.form.get("email").lower()
    password = request.form.get("password")
    user = run_query("SELECT * FROM users WHERE email = ?", (email,))
    user =user[0] if user else None
    if not user or not check_password_hash(user["hashed_password"], password):
        return redirect("/signin")
    session.permanent = True
    session["user_id"] = user["id"]
    return redirect("/home")

@app.post("/signup")
def post_signup():
    full_name = request.form.get("full_name", "")
    email = request.form.get("email", "").lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm", "")
    if password != confirm_password:
        return redirect("/signup")
    try:
        hashed_password = generate_password_hash(password)
        run_query("INSERT INTO users (email, full_name, hashed_password) VALUES (?, ?, ?)",(email, full_name, hashed_password),False)
    except:
        return redirect("/signup")
    user = run_query("SELECT * FROM users WHERE email = ?", (email,))
    user = user[0] if user else None
    session.permanent = True
    session["user_id"] = user["id"]
    return redirect("/home")

@app.get("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.get("/connect")
def get_connect():
    return redirect("/home")

@app.post("/connect")
def post_connect():
    user_id =  session.get("user_id")
    bank_name = request.form.get("bank_name")
    routing_number= int(request.form.get("routing"))
    account_number = int(request.form.get("account"))
    run_query("INSERT INTO bank_accounts (user_id, bank_name, routing_number, account_number) VALUES (?, ?, ?, ?)",(user_id, bank_name, routing_number, account_number), False)
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True, port=5001)