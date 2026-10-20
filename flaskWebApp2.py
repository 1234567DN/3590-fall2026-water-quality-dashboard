from flask import Flask, request, jsonify

app = Flask(__name__)

DATA = [
    {"id":1,"campus":"MMC","lat":25.76057810,"lon":-80.36934121},
    {"id":2,"campus":"BBC","lat":25.90932603,"lon":-80.13842127},
]
next_id = 3

# TODO: Week 10, a route for the status, a route for all the items,
#  route for a specific item (through an id) and
#  create a simple client to request data from this API

@app.route('/')
def index():
    return "<h1>Welcome to my First API</h1>"

if __name__ == '__main__':
    app.run(debug=True,port=5000)