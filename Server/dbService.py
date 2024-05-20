from tinydb import TinyDB, Query
from streamModel import Stream
from userModel import User
class DbService:
    def __init__(self):
      self.userDb = TinyDB('./db/userDb.json')
      self.streamsDb = TinyDB('./db/streamsDb.json')
      self.tokenDb = TinyDB('./db/tokenDb.json')
      self.streamsDb.truncate()
      
    def addUser(self, user : User):
        self.userDb.insert(user)
    def getUser(self, username):
        UserQuery = Query()
        user_data = self.userDb.search(UserQuery.username == username)
        return [User(**data) for data in user_data] if user_data else None
    def getUserByKey(self, streamKey):
        UserQuery = Query()
        user_data = self.userDb.search(UserQuery.streamKey == streamKey)
        return [User(**data) for data in user_data] if user_data else None
    def deleteUser(self, username):
        User = Query()
        self.userDb.remove(User.username == username)
    
    def updateUser(self, username, user):
        User = Query()
        self.userDb.update(user, User.username == username)
        
    def addStream(self, stream):
        self.streamsDb.insert(stream)
    def getStream(self, streamKey):
        StreamQuery = Query()
        stream_data = self.streamsDb.search(StreamQuery.stream_key == streamKey)
        return [Stream(**data) for data in stream_data] if stream_data else None
    def getStreams(self):
        stream_data = self.streamsDb.all()
        return [Stream(**data) for data in stream_data] if stream_data else None
    def closeStream(self, streamKey):
        Stream = Query()
        self.streamsDb.remove(Stream.stream_key == streamKey)

    def addToken(self, token):
        self.tokenDb.insert(token)
    def getToken(self, token):
        TokenQuery = Query()
        token_data = self.tokenDb.search(TokenQuery.token == token)
        return [token for token in token_data] if token_data else None
    