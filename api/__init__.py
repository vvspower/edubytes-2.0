from flask import Flask
from flask_cors import CORS

import pymongo


MONGO_CONNECTION_STRING = "mongodb+srv://vvspower:lenovo123@cluster-e.dfrzsfk.mongodb.net/?retryWrites=true&w=majority"

try:

    mongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = mongo.main
    print("Connected to MongoDB")
    mongo.server_info()

except Exception as ex:

    print(ex)
    print("There was an error connecting to MongoDB")


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .auth import auth
    from .forum import forum

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(forum, url_prefix='/community/forums')

    return app
