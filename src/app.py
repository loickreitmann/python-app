from flask import Flask

app = Flask(__name__)

# '/api/v1/details'
@app.route('/api/v1/details')

# TODO healthz route
# '/api/v1/healthz'

def details():
    return 'Hello Porto'

if __name__ == '__main__':
    app.run()

