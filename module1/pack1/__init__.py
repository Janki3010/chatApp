from flask import Blueprint
from module1 import app, socketio

pack1_bp = Blueprint("module1", __name__)
socketio.blueprint_setup = pack1_bp
socketio.blueprint = pack1_bp


from module1.pack1 import endpoint,resources
app.register_blueprint(pack1_bp)
socketio.on_namespace(resources.ChatApp('/chat'))


