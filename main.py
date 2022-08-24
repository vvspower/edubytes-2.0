from api import create_app
from flask import Flask, Request, Response
from flask_cors import CORS

app = create_app()
CORS(app)


@app.route("/", methods=["GET"])
def hello_world():
    return Response(response="Hello World")


if __name__ == '__main__':
    app.run(debug=True, port=9000)
