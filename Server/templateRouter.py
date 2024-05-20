from flask import Blueprint,render_template, send_from_directory

templates = Blueprint('templates', __name__)


@templates.route('/')
def index():
    return render_template('init.html')
@templates.route('/login')
def auth():
    return render_template('auth.html')
@templates.route('/register')
def register():
    return render_template('register.html')
@templates.route('/home')
def home():
    return render_template('home.html')
@templates.route('/watch/<stream_name>')
def stream(stream_name):
    return render_template('stream.html', streamKey=stream_name)

@templates.route('/img/<filename>')
def send_image(filename):
    return send_from_directory('img', filename)