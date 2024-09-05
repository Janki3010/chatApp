from module1 import api
from module1.pack1.resources import *

api.add_resource(Register, '/reg')
api.add_resource(Login, '/verify')
api.add_resource(Dashboard,'/home')
api.add_resource(SendFriendRequest, '/friend_request')
api.add_resource(ViewFriendRequest, '/view_request')
api.add_resource(AcceptFrdReq, '/accept_request')
api.add_resource(Connections, '/my-friends')

api.add_resource(Logout, '/logout')


