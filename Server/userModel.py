class User:
    def __init__(self, email=None, username=None, password=None, streamKey=None,profilePic=None, **kwargs):
        if kwargs:
            self.username = kwargs.get('username')
            self.password = kwargs.get('password')
            self.email = kwargs.get('email')
            self.streamKey = kwargs.get('streamKey')
            self.profilePic = profilePic
        else:
            self.username = username
            self.password = password
            self.email = email
            self.streamKey = streamKey
            self.profilePic = profilePic
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'streamKey': self.streamKey,
            'profilePic': self.profilePic
        }