import io
import random
import time
import cv2
from flask import Flask,Response, json, send_file
from tinydb import TinyDB, Query
from dbService import DbService
from flask import request,render_template,send_from_directory
from controller import ApiController
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
from helpers import get_random_color, new_stream_background,app,socketio,streamRooms
from templateRouter import templates
from authRouter import auth
from streamRouter import streamRouter
import os


wsClients = {}


app.register_blueprint(templates)
app.register_blueprint(auth)
app.register_blueprint(streamRouter)
 

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('join')
def test_connect(data):
    wsClients[data] = request.sid
    socketio.emit('message', 'Connected', room=wsClients[data])

@socketio.on('joinStream')
def stream(stream_name , user_name):
    color = get_random_color()
    streamRooms[stream_name]['participants'].append({'user_name': user_name, 'sid': request.sid , 'color': color })
    socketio.emit('syncMessages',streamRooms[stream_name]['messages'] , room=request.sid)

@socketio.on('leftStream')
def stream(stream_name , user_name):
    streamRooms[stream_name]['participants'] = [x for x in streamRooms[stream_name]['participants'] if x['user_name'] != user_name]
    socketio.emit('message', 'Connected', room=request.sid)

@socketio.on('sentMessage')
def sent_message(stream_name, message, user_name):
    room_participants = streamRooms.get(stream_name, [])['participants']
    message = {
        'message': message,
        'user_name': user_name,
        'color': [x['color'] for x in room_participants if x['user_name'] == user_name][0]
        }
    streamRooms[stream_name]['messages'].append(message)
    if len(streamRooms[stream_name]['messages']) > 10:
        streamRooms[stream_name]['messages'].pop(0)

    for participant in room_participants:
        participant_sid = participant['sid']
        socketio.emit('newMessage', message , room=participant_sid)
    

@socketio.on('disconnect')
def test_disconnect():
    keys = [k for k, v in wsClients.items() if v == request.sid]
    for key in keys:
        del wsClients[key]


if __name__ == '__main__':
    app.debug = True
    socketio.run(app)