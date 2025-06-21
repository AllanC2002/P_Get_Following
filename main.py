from flask import Flask, request, jsonify
from services.functions import get_following
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

@app.route("/following", methods=["GET"])
def following():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token missing or invalid"}), 401

    token = auth_header.replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")

        if not user_id:
            return jsonify({"error": "Invalid token data"}), 401

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    response, code = get_following(user_id)
    return jsonify(response), code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
