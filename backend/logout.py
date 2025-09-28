from flask import Flask, session, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
app.secret_key = "super_secret_key" 


@app.route("/login", methods=["POST"])
def login():
    session["user_id"] = 1  
    return jsonify({"message": "Login successful"})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None) 
    return jsonify({"message": "Logout successful"})

if __name__ == "__main__":
    app.run(debug=True)
