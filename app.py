from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/status', methods=['GET'])
def get_status():
    from utils.query import get_status
    return get_status()
