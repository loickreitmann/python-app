import socket
from flask import Flask, jsonify
from markupsafe import escape
import datetime

app = Flask(__name__)

# '/'
@app.route("/")
def root():
    return f"Hello, there. It's {datetime.datetime.now().strftime("%A, %B %d, %Y")}. You want to go home and rethink your life."

# '/<name>'
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}. It's {datetime.datetime.now().strftime("%A, %B %d, %Y")}. Don't you want to go home and rethink your life?"

# '/api/v1/details'
@app.route('/api/v1/details')
def details():
    msg = 'Oye beratna! Kowa mi kin help to, kopeng?'
    json_data = {
        "message": msg,
        "time": datetime.datetime.now().strftime("%H:%M:%S on %B %d, %Y"),
        "hostname": socket.gethostname()
    }
    return jsonify(json_data)

# '/api/v1/healthz'
@app.route('/api/v1/healthz')
def health():
    healthy_json = {"status": "up"}
    healthy_code = 200
    return jsonify(healthy_json), healthy_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

