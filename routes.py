from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.find_by_email(data['email']):
        return jsonify({"message": "User already exists"}), 400
    
    User.create_user(data['email'], data['password'])
    return jsonify({"message": "User created successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    
    if not user or not User.verify_password(data['password'], user['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user['email'])
    return jsonify({"access_token": access_token}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "You have accessed a protected route"}), 200
