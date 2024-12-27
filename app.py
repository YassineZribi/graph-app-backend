from flask import Flask, jsonify
from config import Config
from models import mongo
from routes import api_bp, auth_bp, graph_bp, dijekstra_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # This will allow all domains by default
app.config.from_object(Config)

# Initialize MongoDB
mongo.init_app(app)

# Initialize JWT Manager
JWTManager(app)

# Register Blueprints
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(graph_bp)
api_bp.register_blueprint(dijekstra_bp)

# Register the parent Blueprint to the app
app.register_blueprint(api_bp)

@app.route('/')
def home():
    return jsonify(message="Graph App API v 1.0.0")

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'production')
    app.run(debug=(env == 'development'))
