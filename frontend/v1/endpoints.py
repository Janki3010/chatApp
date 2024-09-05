from frontend import api
from frontend.v1.resources import *

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Home, '/home')
api.add_resource(ViewRequest, '/viewRequests')
api.add_resource(MyFriends, '/connection')
api.add_resource(Chat, '/chat/<user_id>')
api.add_resource(Logout, '/logout')

