from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Graph
from utils import serialize_objectid
from dijekstra.dijekstra_service import get_shortest_path

# Create a parent API Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify({"message": "L'utilisateur existe déjà"}), 400
    
    User.create_user(data["first_name"], data["last_name"], data['email'], data['password'])
    return jsonify({"message": "Utilisateur créé avec succès"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    
    if not user or not User.verify_password(data['password'], user['password']):
        return jsonify({"message": "Informations d'identification invalides"}), 401
    
    # Convert the _id to a string before returning
    user['_id'] = serialize_objectid(user['_id'])
    del user['password']
    
    access_token = create_access_token(identity=user['email'])
    return jsonify({"access_token": access_token, "user": user}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "Vous avez accédé à une route protégée"}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_email = get_jwt_identity()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    # Convert the _id to a string before returning
    user['_id'] = serialize_objectid(user['_id'])
    del user['password']
    
    return jsonify(user), 200

graph_bp = Blueprint('graph', __name__)

# Save or Update the user's graph
@graph_bp.route('/graph', methods=['POST'])
@jwt_required()
def save_graph():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    graph = Graph.create_or_update_graph(user['_id'], data)
    if graph:
        # Convert ObjectId to string for serialization
        graph['_id'] = serialize_objectid(graph['_id'])
        return jsonify({"message": "Graphe sauvegardé avec succès", "graph": graph}), 200
    return jsonify({"message": "Erreur lors de l'enregistrement du graphe"}), 500

# Get the user's graph
@graph_bp.route('/graph', methods=['GET'])
@jwt_required()
def get_graph():
    current_user_email = get_jwt_identity()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    graph = Graph.get_graph(user['_id'])
    if graph:
        # Convert ObjectId to string for serialization
        graph['_id'] = serialize_objectid(graph['_id'])
        return jsonify(graph), 200
    return jsonify({"message": "Aucun graphe trouvé pour cet utilisateur"}), 404

# Delete the user's graph
@graph_bp.route('/graph', methods=['DELETE'])
@jwt_required()
def delete_graph():
    current_user_email = get_jwt_identity()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    graph = Graph.get_graph(user['_id'])
    if graph:
        success = Graph.delete_graph(user['_id'])
        if success:
            return jsonify({"message": "Graphe supprimé avec succès"}), 200
        return jsonify({"message": "Erreur lors de la suppression du graphe"}), 500
    return jsonify({"message": "Aucun graphe trouvé pour cet utilisateur"}), 404


dijekstra_bp = Blueprint('dijekstra', __name__)

# Calculate the dijekstra shortest path of the user's graph
@dijekstra_bp.route('/dijekstra', methods=['POST'])
@jwt_required()
def calculate_dijekstra_shortest_path():
    current_user_email = get_jwt_identity()
    data = request.get_json()

    user = User.find_by_email(current_user_email)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    selected_nodes_and_edges = get_shortest_path(data['graph'], data['startNode'], data['endNode'])
    # graph = Graph.get_graph(user['_id'])
    # if graph:
    #     # Convert ObjectId to string for serialization
    #     graph['_id'] = serialize_objectid(graph['_id'])
    #     return jsonify(graph), 200
    return jsonify(selected_nodes_and_edges), 200