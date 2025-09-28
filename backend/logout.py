from flask import Flask, session, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = "super_secret_key"

# Dummy user for demonstration
USER_DB = {"testuser": "testpassword"}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in USER_DB and USER_DB[username] == password:
        session["user_id"] = username
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200

@app.route("/status", methods=["GET"])
def status():
    user_id = session.get("user_id")
    if user_id:
        return jsonify({"logged_in": True, "user": user_id}), 200
    return jsonify({"logged_in": False}), 200

if __name__ == "__main__":
    app.run(debug=True)
