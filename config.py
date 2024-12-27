import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    
    # JWT Expiration Time (1 day)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Uncomment the following line for tokens that never expire
    # JWT_ACCESS_TOKEN_EXPIRES = False
