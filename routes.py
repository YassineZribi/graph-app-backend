from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Graph
from utils import serialize_objectid

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify({"message": "User already exists"}), 400
    
    User.create_user(data["first_name"], data["last_name"], data['email'], data['password'])
    return jsonify({"message": "User created successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    
    if not user or not User.verify_password(data['password'], user['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    
    # Convert the _id to a string before returning
    user['_id'] = serialize_objectid(user['_id'])
    del user['password']
    
    access_token = create_access_token(identity=user['email'])
    return jsonify({"access_token": access_token, "user": user}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "You have accessed a protected route"}), 200


graph_bp = Blueprint('graph', __name__)

# Save or Update the user's graph
@graph_bp.route('/graph', methods=['POST'])
@jwt_required()
def save_graph():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    graph = Graph.create_or_update_graph(user['_id'], data)
    if graph:
        # Convert ObjectId to string for serialization
        graph['_id'] = serialize_objectid(graph['_id'])
        return jsonify({"message": "Graph saved/updated successfully", "graph": graph}), 200
    return jsonify({"message": "Error saving graph"}), 500

# Get the user's graph
@graph_bp.route('/graph', methods=['GET'])
@jwt_required()
def get_graph():
    current_user_email = get_jwt_identity()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    graph = Graph.get_graph(user['_id'])
    if graph:
        # Convert ObjectId to string for serialization
        graph['_id'] = serialize_objectid(graph['_id'])
        return jsonify(graph), 200
    return jsonify({"message": "No graph found for this user"}), 404

# Delete the user's graph
@graph_bp.route('/graph', methods=['DELETE'])
@jwt_required()
def delete_graph():
    current_user_email = get_jwt_identity()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "User not found"}), 404

    success = Graph.delete_graph(user['_id'])
    if success:
        return jsonify({"message": "Graph deleted successfully"}), 200
    return jsonify({"message": "Error deleting graph"}), 500