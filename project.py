from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# -----------------------
# Hash password (Security)
# -----------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------
# Database connection
# -----------------------
def db_connection():
    conn = sqlite3.connect("fractoscan.db")
    conn.row_factory = sqlite3.Row
    return conn


# ============================
# 1) REGISTER ENDPOINT
# ============================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not name or not email or not username or not password:
        return jsonify({"status": "error", "message": "All fields required"}), 400

    hashed_password = hash_password(password)

    conn = db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (name, email, username, password)
            VALUES (?, ?, ?, ?)
        """, (name, email, username, hashed_password))

        conn.commit()
        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Email or Username already exists"}), 409

    finally:
        conn.close()


# ============================
# 2) LOGIN ENDPOINT
# ============================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Email & password required"}), 400

    hashed_password = hash_password(password)

    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, email, username
        FROM users
        WHERE email=? AND password=?
    """, (email, hashed_password))

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": dict(user)
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

# Run Server
if __name__ == "__main__":
    app.run(debug=True, port=9000)
