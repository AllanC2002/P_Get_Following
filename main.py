from flask import Flask, request, jsonify
from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
import jwt
import os
from dotenv import load_dotenv
from resolvers.graphql_resolvers import query
from services.functions import get_following

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

def get_user_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get("user_id")
    except Exception:
        return None

# GraphQL schema + resolvers
type_defs = load_schema_from_path("schema/schema.graphql")
schema = make_executable_schema(type_defs, query)

@app.route("/following", methods=["GET"]) #Rest
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

@app.route("/graphql", methods=["POST"]) #GraphQl
def graphql_server():
    data = request.get_json()
    context = {"request": request, "user_id": get_user_from_token()}
    success, result = graphql_sync( # graphql_sync return two values succes and result
        schema,
        data,
        context_value=context,
        debug=True
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route("/")
def hello():
    return "Rest and GraphQl"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
