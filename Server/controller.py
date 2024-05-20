from flask import json,Response
from dbService import DbService
from streamModel import Stream
from userModel import User
import uuid
class ApiController:
    def __init__(self):
        self.dbService = DbService()

    def createUser(self, email, username, password):
     user = self.dbService.getUser(username)
     if not user:
        streamKey = str(uuid.uuid4())  # Generate a UUID for the stream key
        user = User(email, username, password, streamKey,"")
        self.dbService.addUser(user.to_dict())
        return 'Ok'
     else:
        raise ValueError('Username already exists')

    def authenticateUser(self, username, password):
     user = self.dbService.getUser(username)
     if user:
        if user[0].password == password:
            token = str(uuid.uuid4())
            self.dbService.addToken({'token': token, 'username': username})
            return json.dumps({'token': token})
        else:
            raise ValueError('Invalid Password')
     else:
        raise ValueError('Invalid Username')
    
    def getUser(self, token):
     username = self.dbService.getToken(token)[0]['username']
     users = self.dbService.getUser(username)
     users_dict = users[0].to_dict()
     return json.dumps(users_dict)
    
    def addProfilePic(self, username, profilePic):
        user = self.dbService.getUser(username)
        if user:
            user[0].profilePic = profilePic
            self.dbService.updateUser(username, user[0].to_dict())
            return 'Ok'
        else:
            raise ValueError('Invalid Username')
     
    def removeUser(self, username):
        user = self.dbService.getUser(username)
        if user:
            self.dbService.deleteUser(username)
            return 'Ok'
        else:
            raise ValueError('Invalid Username')
    
    def verifyToken(self, token):
     try:
      token = self.dbService.getToken(token)
      if token:
        return Response("Valid token", status=200)
      else:
        return Response("Invalid token", status=500)
     except:
        return Response("Invalid token", status=500)
        
    def newStream(self, stream_name, stream_id):
        user = self.dbService.getUserByKey(stream_name)
        if user:
            
            stream = Stream("live/"+stream_name,stream_name ,user[0].username ,stream_id)
            stream_dict = stream.to_dict()
            self.dbService.addStream(stream_dict)        
            return 'Ok'
        else:
            raise ValueError('Invalid Stream Key')
        pass
    
    def closeStream(self, stream_name, stream_id):
        stream = self.dbService.getStream(stream_name)
        if stream:  
            self.dbService.closeStream(stream_name)
            return 'Ok'
        else:
            raise ValueError('Invalid Stream Key')
        pass
    
    def getStreams(self):

        streams = self.dbService.getStreams()
        if not streams:
            raise ValueError('No streams available')
             
        streams_dict = [stream.to_dict() for stream in streams]
        for stream in streams_dict:
            user = self.dbService.getUser(stream['streamer_name'])
            if user:
                stream['profilePic'] = user[0].profilePic
            else:
                stream['profilePic'] = 'default.png'  
        return json.dumps(streams_dict)