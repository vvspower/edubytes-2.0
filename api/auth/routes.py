# from .helpers import send_email
from .helpers.functions import check_email_exists, check_username_exists, send_email, initialize_user, get_friends
from .helpers.exceptions import RequiredExists, EmptyField, HTTP_HEADER_MISSING
from xml.dom import NotFoundErr
from api import db
import os
import sys
from bson import ObjectId
from flask import Blueprint, request, Response
import jwt
import bcrypt
import time
import datetime
import calendar
import json

sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

auth = Blueprint('auth', __name__)

JWT_SECRET_KEY = "d445191d82cd77c696de"

try:
    from .models import user_model, notification_model
    db.create_collection("users")
    db.command("collMod", "users", validator={})
    db.create_collection("notifications")
    db.command("collMod", "notifications", validator=notification_model)

    db.create_collection('dead_tokens')

except Exception as ex:
    print(ex)


# ROUTES


@auth.route('/sign-up', methods=["POST"])
def sign_up():
    try:
        content = request.get_json()

        # Checks if any fields are empty
        if content["username"] == "" or content["email"] == "" or content["password"] == "":
            raise EmptyField("Please do not leave field empty")

        # Existence check
        check_email_exists(content["email"])
        check_username_exists(content["username"])

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(content["password"].encode('utf-8'), salt)

        payload = {'username': content["username"], 'email': content["email"], 'password': password.decode(
            'utf-8'), "ip": request.remote_addr, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15), }  # 15 minutes timeout
        token = jwt.encode(payload=payload, key=JWT_SECRET_KEY)

        # ? Covert code to send email instead of return auth token
        send_email(content["email"], token)

        return Response(response=json.dumps({"data": "Email has been send", "success": True}), status=200, mimetype="applcation/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="applcation/json")
    except jwt.ExpiredSignatureError:
        return Response(response=json.dumps({"data": "token is expired", "success": False}), status=401, mimetype="applcation/json")
    except RequiredExists as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=403, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="applcation/json")


# VERIFY USER


@auth.route('/sign-up/verify', methods=["POST"])
def verify_user():
    try:

        token = request.headers["Authorization"]
        print(token)

        dbResponse = db.dead_tokens.find_one({"token": token})
        if dbResponse == None:
            db.dead_tokens.insert_one({"token": token})
            payload = jwt.decode(
                jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])

            presentDate = datetime.datetime.now()
            print(payload["password"].encode('utf-8'))

            user = initialize_user(payload)
            print(user)

            dbResponse = db.users.insert_one(user)
            payload = {'user_id': str(dbResponse.inserted_id)}
            token = jwt.encode(payload=payload, key=JWT_SECRET_KEY)
            return Response(response=json.dumps({"data": token, "success": True}), status=200, mimetype="applcation/json")
        else:
            raise Exception("Token is dead")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="applcation/json")


# LOGIN USER

@auth.route('/sign-in', methods=["POST"])
def login_user():
    try:
        content = request.get_json()

        if content["email"] == "" or content["password"] == "":
            raise EmptyField("Please do not leave field empty")

        dbResponse = db.users.find_one({"email": content["email"]})
        print(dbResponse)
        if dbResponse == None:
            raise NotFoundErr("invalid credentials")

        success = bcrypt.checkpw(content["password"].encode(
            'utf-8'), dbResponse["password"])
        if success:
            dbResponse['_id'] = str(dbResponse['_id'])
            payload = {
                "user_id": dbResponse['_id']
            }
            token = jwt.encode(payload=payload, key=JWT_SECRET_KEY)

            return Response(response=json.dumps({"data": token, "success": True}), status=200, mimetype="applcation/json")
        else:
            return Response(response=json.dumps({"data": "incorrect credentials"}), status=400, mimetype="applcation/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="applcation/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="applcation/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="applcation/json")


# GET USER

@auth.route("/user/<username>", methods=['GET'])
# USE IF GETTING USER USING AUTH TOKEN ONLY
@auth.route('/user', methods=['GET'], defaults={'username': None})
def check_user(username):
    try:
        if username == None:
            token = request.headers['Authorization']
            print(token)

            if token == "":
                raise HTTP_HEADER_MISSING("Auth-token missing")
            payload = jwt.decode(
                jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
            user = db.users.find_one(
                {"_id": ObjectId(payload["user_id"])})
            user['_id'] = str(user['_id'])
            del user["password"]

        else:
            user = db.users.find_one({"username": username})
            if user == None:
                raise NotFoundErr("User not found")

            user['_id'] = str(user['_id'])
            del user["password"]

            print(user["username"])

        friends = get_friends(user["username"])
        user["friends"] = friends

        return Response(response=json.dumps({"data": user, "success": True}), status=200, mimetype="applcation/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="applcation/json")
    except HTTP_HEADER_MISSING as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=401, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": "Something went wrong", "success": False}), status=500, mimetype="applcation/json")


# UPDATE USER

@auth.route("/user", methods=["PUT"])
def update_user():
    try:
        token = request.headers['Authorization']
        print(token, "hello")
        if token == "":
            raise HTTP_HEADER_MISSING("auth-token missing")
        content = request.get_json()
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

        dbResponse = db.users.update_one({"_id": ObjectId(
            payload["user_id"])}, {"$set": {"details": content["details"], "education": content["education"]}})
        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"data": "Updated", "success": True}), status=200, mimetype="applcation/json")
        else:
            return Response(response=json.dumps({"data": "Nothing to update", "success": True}), status=200, mimetype="applcation/json")
    except HTTP_HEADER_MISSING as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": "Update failed", "success": False}), status=500, mimetype="applcation/json")
