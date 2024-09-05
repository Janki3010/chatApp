from flask import Flask
from flask_restful import Api
import importlib

app = Flask(__name__, template_folder="../templates",static_folder='../static')
api = Api(app)

importlib.import_module('frontend.v1')
