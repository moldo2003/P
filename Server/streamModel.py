class Stream:
    def __init__(self, stream_url=None, stream_key=None, streamer_name=None, stream_id=None, **kwargs):
        if kwargs:
            self.stream_url = kwargs.get('stream_url')
            self.stream_key = kwargs.get('stream_key')
            self.streamer_name = kwargs.get('streamer_name')
            self.stream_id = kwargs.get('stream_id')
        else:
            self.stream_url = stream_url
            self.stream_key = stream_key
            self.streamer_name = streamer_name
            self.stream_id = stream_id
    def to_dict(self):
        return {
            'stream_url': self.stream_url,
            'stream_key': self.stream_key,
            'streamer_name': self.streamer_name,
            'stream_id': self.stream_id
        }