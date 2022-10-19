from flask import Flask
from flask_cors import CORS

import pymongo


MONGO_CONNECTION_STRING = "mongodb+srv://vvspower:lenovo123@cluster-e.dfrzsfk.mongodb.net/?retryWrites=true&w=majority"

try:

    mongo = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = mongo.main
    db_events = mongo.events
    print("Connected to MongoDB")
    mongo.server_info()

except Exception as ex:

    print(ex)
    print("There was an error connecting to MongoDB")


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .auth.routes import auth
    from .forum.routes import forum
    from .suggestions.routes import suggestions
    from .friend_sys.routes import friend
    from .events.notifications.routes import notification

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(forum, url_prefix='/community/forums')
    app.register_blueprint(suggestions, url_prefix='/suggestions')
    app.register_blueprint(friend, url_prefix='/friend')
    app.register_blueprint(notification, url_prefix='/notifications')

    return app
