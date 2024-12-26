from flask import Flask
from config import Config
from models import mongo
from routes import auth
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo.init_app(app)

# Initialize JWT Manager
JWTManager(app)

# Register Blueprint
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
