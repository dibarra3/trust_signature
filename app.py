import os
import sqlite3
import base64
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
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    user = run_query("SELECT id, email, full_name, phone FROM users WHERE id = ?", (user_id,))
    if user:
        user = user[0]
    else:
        user = {}
    return render_template("profile.html", user=user)

@app.get("/contact")
def get_contact():
    return render_template("contact.html")

@app.get("/signin")
def get_signin():
    return render_template("signin.html")

@app.get("/signup")
def get_signup():
    return render_template("signup.html")

@app.get("/signature")
def get_signature():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    signatures = get_signatures(user_id)
    return render_template("signature.html", signatures=signatures)


def get_signatures(user_id):
    return run_query("SELECT id, image_base64, label FROM signatures WHERE user_id = ? ORDER by id DESC", (user_id,))

@app.post("/profile")
def post_profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    username = request.form.get("username","")
    email = request.form.get("email","")
    phone= request.form.get("phone","")
    run_query("UPDATE users SET full_name=?, email=?, phone=? WHERE id=?", (username, email, phone,user_id), fetch=False)
    return redirect("/profile")

@app.post("/signature/save")
def save_signature():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    data_url = request.form.get("data_url")
    file = request.files.get("file")
    label = request.form.get("label") or "Custom"
    image = None
    if data_url and data_url[:11] == "data:image/":
        image = data_url.split(",",1)[1]
    elif file and file.filename:
        image = base64.b64encode(file.read()).decode("utf-8")
    else:
        return redirect("/signature")
    run_query("INSERT INTO signatures (user_id, image_base64,label) VALUES (?,?, ?)", (user_id, image,label), fetch=False)
    return render_template("signature_preview.html", image_url = "data:/png;base64,"+image)


@app.get("/transfer")
def get_transfer():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    bank_accounts = run_query("SELECT * FROM bank_accounts WHERE user_id =?", (user_id,))
    signatures = run_query("SELECT * FROM signatures WHERE user_id =?", (user_id,))
    return render_template("transfer.html", bank_accounts=bank_accounts, signatures= signatures)

@app.post("/transfer")
def post_transfer():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    acc_id = int(request.form.get("account_id"))
    sign_id = int(request.form.get("signature_id"))
    recipient = request.form.get("recipient")
    amt = float(request.form.get("amount"))
    date = request.form.get("date")
    run_query("INSERT INTO PAYMENTS (user_id, account_id, signature_id, recipient, status,amount, date) VALUES (?,?,?,?,?,?,?)",(user_id,acc_id,sign_id,recipient,"CONFIRMED",amt,date),False)
    payment_id = run_query("SELECT last_insert_rowid() AS last_row", fetch=True)[0]
    payment_id = payment_id["last_row"]
    return redirect(f"/transfer_preview/{payment_id}")


@app.get("/transfer_preview/<int:payment_id>")
def get_transfer_preview(payment_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    payment_info = run_query("SELECT * FROM payments WHERE id=? AND user_id=?",(payment_id, user_id))
    if not payment_info:
        return redirect("/payment")
    payment_info = payment_info[0]
    signature_id = payment_info["signature_id"]
    signature_info = run_query("SELECT * FROM signatures WHERE id=? AND user_id=?", (signature_id, user_id))
    if not signature_info:
        return redirect("/payments")
    
    signature = signature_info[0]
    image_base64 = signature["image_base64"]
    #print(signature["image_base64"])
    return render_template("transfer_preview.html", payment = payment_info, image_url = "data:/png;base64,"+ image_base64)

@app.get("/payments/<int:payment_id>")
def get_payment_id(payment_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    payment_info = run_query("SELECT * FROM payments WHERE id=? AND user_id=?",(payment_id, user_id))
    if not payment_info:
        return redirect("/payment")
    payment_info = payment_info[0]
    signature_id = payment_info["signature_id"]
    signature_info = run_query("SELECT * FROM signatures WHERE id=? AND user_id=?", (signature_id, user_id))
    if not signature_info:
        return redirect("/payments")
    
    signature = signature_info[0]
    image_base64 = signature["image_base64"]
    #print(signature["image_base64"])
    return render_template("view_transfer.html", payment = payment_info, image_url = "data:/png;base64,"+ image_base64)


@app.get("/payments")
def get_payments():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/signin")
    payments = run_query("SELECT * FROM payments WHERE user_id =? ORDER BY id DESC",(user_id,))
    return render_template("transfers.html", payments=payments)


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
    try:
        routing_number= int(request.form.get("routing"))
    except:
        routing_number = 1234567

    try:
        account_number = int(request.form.get("account"))
    except:
        account_number = 7654321
    run_query("INSERT INTO bank_accounts (user_id, bank_name, routing_number, account_number) VALUES (?, ?, ?, ?)",(user_id, bank_name, routing_number, account_number), False)
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True, port=5001)