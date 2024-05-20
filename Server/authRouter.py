

import os
from flask import Flask, request, Response,Blueprint
from controller import ApiController
from werkzeug.utils import secure_filename

controller = ApiController()

auth = Blueprint('auth', __name__)

@auth.route('/createUser' , methods=['POST'])
def create_user():
    data = request.get_json()
    #email = data.get('email')
    email = ""
    password = data.get('password')
    name = data.get('name')
    try:
        controller.createUser(email, name, password)
        return Response('User created', status=200)
    except Exception as e:
        return Response(str(e), status=500)
    

@auth.route('/authenticateUser' , methods=['POST'])
def authenticate_user():
    data = request.get_json()
    password = data.get('password')
    name = data.get('name')
    try:
        return controller.authenticateUser(name, password)
    except Exception as e:
        return Response(str(e), status=500)


@auth.route('/getUser/<token>' , methods=['GET'])
def get_user(token):
    return controller.getUser(token)

@auth.route('/verifyToken' , methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    return controller.verifyToken(token)

@auth.route('/uploadImage', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    username = request.form['username']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        if not os.path.exists('img'):
            os.makedirs('img')
        file.save(os.path.join('img', filename))
        controller.addProfilePic(username, filename)
        return 'File uploaded successfully', 200