import socket
from flask import Flask, jsonify
import datetime

app = Flask(__name__)

# '/api/v1/details'
@app.route('/api/v1/details')
def details():
    msg = 'Hello there, Porto!'
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
    app.run()

