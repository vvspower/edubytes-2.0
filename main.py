from api import create_app
from flask import Flask, Request, Response

app = create_app()


@app.route("/", methods=["GET"])
def hello_world():
    return Response(response="Hello World")


if __name__ == '__main__':
    app.run(debug=True, port=9000)
