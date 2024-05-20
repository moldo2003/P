import random
import time

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

streamRooms = {}

def new_stream_background(stream_name, stream_id):
    time.sleep(10)  
    socketio.emit('newStream', "New Stream") 

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgb({r},{g},{b})'