import hashlib
import json
import re
import time
from datetime import datetime
from uuid import uuid4

from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Resource
from flask import request
from flask_socketio import Namespace, emit, join_room, leave_room
from module1 import mysql, r, es
from module1.pack1.models import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def validate_password(password):
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return re.match(pattern, password) is not None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class Register(Resource):
    def post(self):
        try:
            print("entered")
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed_password = hash_password(password)
            print(username, email, password)
            # profilepic = request.files['profilepic']
            new_user = User(username=username, email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

            return {"msg": "registered", 'data': None}, 200
        except KeyError as e:
            return {"msg": "error", "error_details": str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {"msg": "error", "error_details": str(e)}, 500


access_token = ''


class Login(Resource):

    def post(self):
        # data = request.json
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)
        user = User.query.filter_by(email=email).first()
        # user1 = User.query.filter_by(username=data['username']).first()
        # {email : {}}
        # data = {
        #     'id': user.id
        # }
        # rds.set(user.email, json.dumps(data))
        # print(rds.get(user.id))
        if user:
            if hashed_password == user.password:
                # session['user_id'] = user.id
                global access_token
                access_token = create_access_token(identity=user.id)
                data = {
                    'id': user.id,
                    'name': user.username,
                    'access_token': access_token
                }
                # r.set(f"{access_token}", json.dumps(data))
                r.set(f"{user.email}", json.dumps(data))
                # return jsonify(access_token=access_token), 200
                return {"msg": "loggedin",
                        'data': {'access_token': access_token, 'id': user.id, 'name': user.username}}, 200
                # return {"msg": "loggedin", 'data': data}, 200

            else:
                return {"msg": "Password does not match", 'data': None}, 400
        else:
            return {"msg": "user not exist", 'data': None}, 404


class Dashboard(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            cur = mysql.connection.cursor()
            cur.callproc('user_requested_data')
            data = cur.fetchall()
            filtered_data = [row for row in data if row[0] != current_user]
            print(filtered_data)
            return {"msg": "success", "data": filtered_data}, 200
        except NoAuthorizationError as e:
            return {"msg": "error", "error_details": "Authorization header is missing or incorrect"}, 401
        except Exception as e:
            return {"msg": "error", "error_details": str(e)}, 500


class SendFriendRequest(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()

        if current_user_id:
            receiver_id = int(request.json.get('friend_id'))
            friend = User.query.filter_by(id=receiver_id).first()

            if friend:
                # Check if a request already exists from current_user_id to receiver_id
                existing_request = Requests.query.filter_by(sender_id=current_user_id, receiver_id=receiver_id).first()

                if existing_request:
                    return {"msg": "Friend request already sent to this user"}, 400

                new_request = Requests(sender_id=current_user_id, receiver_id=receiver_id)
                db.session.add(new_request)
                db.session.commit()

                cur = mysql.connection.cursor()
                cur.callproc('user_requested_data')
                data = cur.fetchall()
                filtered_data = [row for row in data if row[0] != current_user_id]
                print(filtered_data)
                return {"msg": "Friend Request is Sent Successfully", "data": filtered_data}, 200
            else:
                return {"msg": "Receiver user not found"}, 404
        else:
            return {"msg": "User not logged in"}, 401


class ViewFriendRequest(Resource):
    @jwt_required()
    def post(self):

        current_user_id = get_jwt_identity()

        if current_user_id:
            cur = mysql.connection.cursor()
            cur.callproc('get_friend_request', [current_user_id])
            data = cur.fetchall()
            return {'msg': 'success', 'data': data}, 200
        else:
            return {"msg": "No friend requests found for the user"}, 404


class AcceptFrdReq(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        if current_user_id:
            request_id = request.json.get('request_id')

            if request_id:
                request_entry = Requests.query.filter_by(sender_id=request_id, receiver_id=current_user_id).first()
                request_entry.status = 1

                new_friend1 = Friends(user_id=current_user_id, friend_id=request_id)
                db.session.add(new_friend1)
                db.session.commit()
                new_friend2 = Friends(user_id=request_id, friend_id=current_user_id)
                db.session.add(new_friend2)
                db.session.commit()

                if current_user_id:
                    cur = mysql.connection.cursor()
                    cur.callproc('get_friend_request', [current_user_id])
                    data = cur.fetchall()
                    return {'msg': 'success', 'data': data}, 200
            else:
                return {"msg": "error"}, 404
        else:
            return {"msg": "User not logged in"}, 401


class Connections(Resource):
    @jwt_required()
    def post(self):

        current_user_id = get_jwt_identity()

        if current_user_id:
            # Fetch list of friends for the current user
            friends = Friends.query.filter_by(user_id=current_user_id).all()

            # Prepare the response data
            friends_list = []
            cur = mysql.connection.cursor()
            for friend in friends:
                cur.callproc('fetch_usernmae', [friend.friend_id])
                data = cur.fetchone()
                friend_data = {
                    'id': friend.friend_id,
                    'username': data[0],
                    'email': data[1]
                }
                friends_list.append(friend_data)

            cur.close()

            # return {'msg': 'success',}, 200
            return {'msg': 'success', 'data': friends_list}, 200
        else:
            return {"msg": "User not logged in"}, 401


class ChatApp(Namespace):

    def on_connect(self):
        user_id = request.args.get('user_id')
        friend_id = request.args.get('friend_id')
        user_name = request.args.get('u_name')
        friend_name = request.args.get('f_name')
        if not user_id or not friend_id:
            return False

        room = f"chat_{min(user_id, friend_id)}_{max(user_id, friend_id)}"
        join_room(room)

        query = {
            'query': {
                'match': {
                    'room': room
                }
            },
            'sort': [
                {'@timestamp': {'order': 'asc'}}
            ]
        }
        response = es.search(index='chat11', body=query)
        chat_history = [{'uname': doc['_source']['uname'], 'message': doc['_source']['message']} for doc in
                        response['hits']['hits']]

        emit('chat_history', chat_history, room=room)
        emit('message', {'msg': f"User {user_name} has entered the chat with {friend_name}"}, room=room)

    def on_message(self, data):
        user_id = request.args.get('user_id')
        friend_id = request.args.get('friend_id')
        user_name = request.args.get('u_name')
        msg = data.get('msg')
        if not user_id or not friend_id or not msg:
            return False

        room = f"chat_{min(user_id, friend_id)}_{max(user_id, friend_id)}"

        document = {
            'uname': user_name,
            'room': room,
            'message': msg,
            '@timestamp': datetime.utcnow()
        }
        es.index(index='chat11', body=document)
        emit('message', {'msg': f"{user_name}: {msg}"}, room=room)


class Logout(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        global access_token
        access_token = ''
        if access_token != '':
            return {'msg': 'error', 'data': {}}, 400
        else:
            return {'msg': 'success', 'data': {}}, 200
