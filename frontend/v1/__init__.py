from frontend import api, app
from flask import Blueprint

wppBluePrint = Blueprint('frontend', __name__)
api.blueprint_setup = wppBluePrint
api.blueprint = wppBluePrint

from frontend.v1 import endpoints

app.register_blueprint(wppBluePrint)

