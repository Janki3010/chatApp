import requests as requests
from flask_restful import Resource
from flask import render_template,make_response,request


class Login(Resource):

    def get(self):
        return make_response(render_template('login.html'))



class Register(Resource):

    def get(self):
        return make_response(render_template('register.html'))

class Home(Resource):

    def get(self):
        # response =requests.get(url="http://127.0.0.1:3050/home")
        # print(response)
        return make_response(render_template('home.html'))


class ViewRequest(Resource):
    def get(self):
        return make_response(render_template('viewrequests.html'))


class MyFriends(Resource):
    def get(self):
        return make_response(render_template('friends.html'))

    # def post(self):
    #     token = request.headers.get('Authorization')
    #     headers = {
    #         "Authorization": token,
    #         "Content-Type": "application/json"
    #     }
    #     res = requests.post('http://127.0.0.1:3050/my-friends', data=None, headers=headers)
    #
    #     print(request)
    #     pass


class Chat(Resource):
    def get(self, user_id):
        return make_response(render_template('chat.html', id=user_id))




class Logout(Resource):
    def get(self):
        return make_response(render_template('logout.html'))
