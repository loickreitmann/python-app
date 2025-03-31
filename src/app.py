from flask import Flask, jsonify

app = Flask(__name__)

# '/api/v1/details'
@app.route('/api/v1/details')

# TODO healthz route
# '/api/v1/healthz'

def details():
    msg = 'Hello there, Porto!'
    json_data = {"message": msg}
    return jsonify(json_data)

if __name__ == '__main__':
    app.run()

