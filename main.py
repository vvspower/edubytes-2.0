from api import create_app
from flask import Flask, Request, Response
from flask_cors import CORS, cross_origin
import os

app = create_app()
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin(supports_credentials=True)
@app.route("/", methods=["GET"])
def hello_world():
    return Response(response="Hello World")


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

# TODO : Create test cases
# with app.test_client() as c:
#     rv = c.post('/api/auth', json={
#         'username': 'flask', 'password': 'secret'
#     })
#     json_data = rv.get_json()
#     assert verify_token(email, json_data['token'])
