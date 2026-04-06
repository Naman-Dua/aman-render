from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔥 CONNECT MONGODB
client = MongoClient("mongodb+srv://NamanAdmin:%40namanD0102@cluster0.h3cucro.mongodb.net/?appName=Cluster0")
db = client["amanelectronics"]

users = db["users"]
cart = db["cart"]

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    users.insert_one({
        "username": data["username"],
        "password": data["password"]
    })

    return jsonify({"message": "User created ✅"})

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        if not data:
            return jsonify({"status": "fail", "message": "No data"}), 400

        user = users.find_one({
            "username": data.get("username"),
            "password": data.get("password")
        })

        if user:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
# ADD TO CART (DB)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json

    cart.insert_one({
        "username": data["username"],
        "name": data["name"],
        "price": data["price"]
    })

    return jsonify({"message": "Added to cart 🛒"})

# GET CART (DB)
@app.route('/get_cart', methods=['POST'])
def get_cart():
    data = request.json

    items = cart.find({"username": data["username"]})

    result = []
    for i in items:
        result.append({
            "name": i["name"],
            "price": i["price"]
        })

    return jsonify(result)

@app.route('/')
def home():
    return "Backend is running ✅"

if __name__ == "__main__":
    app.run()