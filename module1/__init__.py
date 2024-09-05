from elastic_transport import NodeConfig
from flask_socketio import SocketIO
from flask import Flask
from flask_restful import Api
import importlib
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from elasticsearch import Elasticsearch


options = {
    'scheme': 'http',
    'host': '192.168.1.21',
    'port': 9200,
}
node_config = NodeConfig(**options)
es = Elasticsearch([node_config])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatApp secret key!'
api = Api(app)


# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, async_mode='eventlet', logger=True, engineio_logger=True, ping_interval=20,
                    always_connect=True, origins=["http://127.0.0.1:3008"], cors_allowed_origins="*")

# CORS(app, resources={r"/verify": {"origins": "http://127.0.0.1:3008"}})
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/facebook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REDIS_URL'] = "redis://localhost:6379/0"
db = SQLAlchemy(app)
r = FlaskRedis(app)
jwt = JWTManager(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'facebook'
mysql = MySQL(app)
# List to store revoked tokens
revoked_tokens = set()




importlib.import_module('module1.pack1')

