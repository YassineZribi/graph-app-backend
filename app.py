from flask import Flask
from config import Config
from models import mongo
from routes import auth, graph_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo.init_app(app)

# Initialize JWT Manager
JWTManager(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(graph_bp)

if __name__ == '__main__':
    app.run(debug=True)
