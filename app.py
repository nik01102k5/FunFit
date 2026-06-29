from flask import Flask, render_template, url_for, redirect
import json
import os
from flask import request,flash,session
import uuid
from flask import send_from_directory, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import main


app = Flask(__name__)

app.secret_key = "secret-key"

# Add below your imports
water_data = {
    "intake": 0,
    "goal": 3
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

@app.route('/')
def index():
    # uName = session.get('userName').capitalize()
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        users = load_users()

        for user in users:
            print(f"if {user['email']} == {email} and {user['password']} == {password}:")

            if user["email"] == email and user["password"] == password:
                
                # 🔐 create session
                session["user"] = {
                    "email": user["email"],
                    "name": user["name"]
                }

                return redirect("/")   # or "/"
        print("Entered:", email, password)
        print("Users:", users)
        return "Invalid email or password"

    return render_template("login.html")
@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")

@app.route('/api/water', methods=['GET'])
def get_water():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if "water" not in session:
        session["water"] = {
            "intake": 0,
            "goal": 3,
            "completed": False
        }

    return jsonify(session["water"])

@app.route('/api/water', methods=['POST'])
def update_water():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if "water" not in session:
        session["water"] = {
            "intake": 0,
            "goal": 3,
            "completed": False
        }

    water = session["water"]
    water["intake"] = data.get("intake", water["intake"])

    reward = False

    # 🎯 Completion check
    if water["intake"] >= water["goal"] and not water["completed"]:
        water["completed"] = True
        reward = True

        session["points"] = session.get("points", 0) + 10

    session["water"] = water

    return jsonify({
        "data": water,
        "reward": reward,
        "points": session.get("points", 0)
    })

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/game')
def game():
    return render_template("game.html")

@app.route('/loading')
def loading():
    return render_template("loading.html")

@app.route('/diet')
def diet():
    return render_template("diet.html")

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    try:
        if request.method == 'POST':
            data = request.get_json(force=True)
            user_input = data.get("message")
            if not user_input:
                return jsonify({"error": "No message"}), 400
            return main.stream_response(user_input)

        # ✅ GET: render chatbot page
        return render_template("chatbot.html")

    except Exception as e:
        print("Error in /chat:", e)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/calorie',methods = ['POST', 'GET'])
def calorie():
    return render_template("calories.html")
    
if __name__ == "__main__":
    app.run(debug=True)