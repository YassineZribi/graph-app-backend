from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo

mongo = PyMongo()

class User:
    @staticmethod
    def create_user(email, password):
        hashed_password = generate_password_hash(password)
        user = {
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
