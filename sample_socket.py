# We need to import request to access the details of the POST request
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    FLASK_PORT = 8000
    app.run(
        host="0.0.0.0",
        port=int(FLASK_PORT)
    )

