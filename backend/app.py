from flask import Flask, request, jsonify
from flask_cors import CORS
from models import create_user, authenticate

app = Flask(__name__)
CORS(app)

# -----------------------------
# Signup Route
# -----------------------------
@app.post("/signup")
def signup():
    data = request.get_json()

    username = data.get("username")
    # FIX: Retrieve the email from the request
    email = data.get("email")
    password = data.get("password")

    # FIX: Include email in the validation
    if not username or not email or not password:
        return jsonify({"success": False, "message": "Username, email, and password are required."}), 400

    # FIX: Pass the email to the create_user function
    success, message = create_user(username, email, password)
    return jsonify({"success": success, "message": message})

# -----------------------------
# Login Route
# -----------------------------
@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    success, message = authenticate(username, password)
    return jsonify({"success": success, "message": message})

# -----------------------------
# Run the server
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
