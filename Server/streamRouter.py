import io
import cv2
from flask import Blueprint, Response, send_file
from helpers import get_random_color, new_stream_background, socketio,streamRooms
from controller import ApiController

streamRouter = Blueprint('streamRouter', __name__)
controller = ApiController()
rtmp_link = 'rtmp://localhost:1935/live/'

@streamRouter.route('/newStream/<stream_name>/<stream_id>')
def new_stream(stream_name,stream_id):
    try:
        res = controller.newStream(stream_name, stream_id)
        if res == 'Ok':
            streamRooms[stream_name] = {'messages': [] , 'participants': []}
            socketio.start_background_task(new_stream_background, stream_name, stream_id)
        return res
    except Exception as e:
        return str(e)
@streamRouter.route('/streamClosed/<stream_name>/<stream_id>')
def stream_cloased(stream_name,stream_id):
    print("streamCloased")
    try:
        res = controller.closeStream(stream_name, stream_id)
        if res == 'Ok':
         socketio.emit('streamCloased', "streamCloased")
         room_participants = streamRooms.get(stream_name['participants'], [])
         for participant in room_participants:
            participant_sid = participant['sid']
            socketio.emit('streamCloased', "streamCloased", room=participant_sid)

        return res
    except Exception as e:
        return str(e)

@streamRouter.route('/getStreams')
def get_streams():
    try:
        return controller.getStreams()
    except Exception as e:
        return Response(str(e), status=500)

@streamRouter.route('/getThumbnail/<stream_name>')
def get_thumbnail(stream_name):

    cap = cv2.VideoCapture(rtmp_link + stream_name)

    if not cap.isOpened():
        return "Error: Unable to open stream", 404

    # Read a frame from the stream
    ret, frame = cap.read()

    if not ret:
        return "Error: Unable to read frame from stream", 404

    # Release the capture object
    cap.release()

    # Convert the frame to JPEG format
    _, jpeg = cv2.imencode('.jpg', frame)
 
    # Send the JPEG image to the client
    return send_file(
        io.BytesIO(jpeg.tobytes()),
        mimetype='image/jpeg'
    )