from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from utils import serialize_objectid

mongo = PyMongo()

class User:
    @staticmethod
    def create_user(first_name, last_name, email, password):
        hashed_password = generate_password_hash(password)
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password
        }
        mongo.db.users.insert_one(user)
        return user

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})
    
    @staticmethod
    def verify_password(password, hashed_password):
        return check_password_hash(hashed_password, password)

class Graph:
    @staticmethod
    def create_or_update_graph(user_id, data):
        graph = mongo.db.graphs.find_one({"user_id": user_id})
        
        if graph:
            # Update the existing graph
            mongo.db.graphs.update_one({"_id": graph['_id']}, {"$set": data})
            graph = mongo.db.graphs.find_one({"user_id": user_id})
        else:
            # Create a new graph
            data['user_id'] = user_id  # Add the user_id to the graph
            graph = mongo.db.graphs.insert_one(data).inserted_id
            graph = mongo.db.graphs.find_one({"_id": graph})

        # Convert ObjectId to string for all fields
        graph = {key: serialize_objectid(value) for key, value in graph.items()}
        return graph

    @staticmethod
    def get_graph(user_id):
        graph = mongo.db.graphs.find_one({"user_id": user_id})
        if graph:
            graph = {key: serialize_objectid(value) for key, value in graph.items()}
        return graph

    @staticmethod
    def delete_graph(user_id):
        result = mongo.db.graphs.delete_one({"user_id": user_id})
        return result.deleted_count > 0
