# We need to import request to access the details of the POST request
from flask import Flask, request
import json

# Openstack credentials
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    data = request.json
    msg= json.dumps(data)
    print(msg)

if __name__ == '__main__':
    FLASK_PORT = 8000
    app.run(
        host="0.0.0.0",
        port=int(FLASK_PORT)
    )
