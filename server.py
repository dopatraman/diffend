from urllib.parse import unquote
import json
from flask import Flask, send_from_directory, jsonify, render_template
from main import run_conversation, get_diff

app = Flask(__name__, static_folder='./static')

@app.route('/static/<path:filename>')  
def send_file(filename):  
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/<author>/<repo>/<base>/<head>')
def begin_workflow(author, repo, base, head):
    base_ = unquote(unquote(base))
    head_ = unquote(unquote(head))
    resp = run_conversation(head)
    return render_template('index.html', repo=repo, author=author, base=base_, head=head_, diff_json=resp)

if __name__ == '__main__':
    app.run(port=8080)
