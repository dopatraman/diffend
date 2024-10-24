from urllib.parse import unquote
from flask import Flask, send_from_directory, jsonify
from main import run_conversation

app = Flask(__name__, static_folder='./static')

@app.route('/static/<path:filename>')  
def send_file(filename):  
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/diff/<base>/<head>')
def diff(base, head):
    # Flash / WSGI interprets all slashes as path params. All branches
    # with slashes get interpreted this way. Double encoding is a hack
    # but a quick way out. The better way to do this is to set AllowEncodedSlashes
    # to On in a WSGI config somewhere.
    base_ = unquote(unquote(base))
    head_ = unquote(unquote(head))
    # return f"{base_}/{head_}"
    return jsonify(run_conversation(head))

if __name__ == '__main__':
    app.run(port=8080)