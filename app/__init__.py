from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import pickle

# init Flask app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# load model to app
with open('linear_regression_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

from app import routes