from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

class User:
    @staticmethod
    def create_user(email, password):
        hashed_password = generate_password_hash(password)
        user = {
            "email": email,
            "password": hashed_password,
            "graph": None  # Each user can have one graph (None means no graph)
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
    def create_or_update_graph(user_id, graph_data):
        # Check if the user already has a graph
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        
        graph = {
            "nodes": graph_data['nodes'],
            "edges": graph_data['edges']
        }

        if user['graph']:
            # Update existing graph
            mongo.db.graphs.update_one(
                {"_id": user['graph']}, 
                {"$set": graph}
            )
            return mongo.db.graphs.find_one({"_id": user['graph']})
        else:
            # Create a new graph
            result = mongo.db.graphs.insert_one(graph)
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, 
                {"$set": {"graph": result.inserted_id}}
            )
            return mongo.db.graphs.find_one({"_id": result.inserted_id})

    @staticmethod
    def get_graph(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user or not user.get('graph'):
            return None
        return mongo.db.graphs.find_one({"_id": user['graph']})

    @staticmethod
    def delete_graph(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if not user or not user.get('graph'):
            return False
        mongo.db.graphs.delete_one({"_id": user['graph']})
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"graph": None}}
        )
        return True
