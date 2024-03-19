from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import pickle
from flask_cors import CORS


# init Flask app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes
resources={r"/add_course": {"origins": "http://127.0.0.1:5501"}}

# load model to app
with open('linear_regression_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

from app import routes