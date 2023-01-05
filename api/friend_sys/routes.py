from flask import Flask, Blueprint, request, Response
import json
from bson import ObjectId
import jwt
import sys
import os
from api import db
from ..events.notifications.functions import on_sending_friend_request, on_del_or_accept_friend_req
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

friend = Blueprint("friend", __name__)
JWT_SECRET_KEY = "d445191d82cd77c696de"


try:
    from .models import friend_model, friend_req_send_model
    db.create_collection("friend")
    db.command("collMod", "friend", validator=friend_model)
    db.create_collection("friend_requests")
    db.command("collMod", "friend_requests", validator=friend_req_send_model)
except Exception as ex:
    print(ex)


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


# send friend request


@friend.route("/request/<username>", methods=["POST"])
def send_friend_request(username):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        reciever_user = username

        if user == reciever_user:
            raise Forbidden("Cannot add friend to yourself")

        if db.friend_requests.find_one({"sender": user, "recipient": reciever_user}) is not None:
            raise Unauthorized("friend request already sent")
        else:
            on_sending_friend_request(reciever_user, user)
            friend = {
                "sender": user,
                "recipient": reciever_user
            }

        if db.friend.find_one({"$or": [{"user_1": user, "user_2": reciever_user}, {"user_1": reciever_user, "user_2": user}]}) != None:
            raise Forbidden("you are already friends")

        dbResponse = db.friend_requests.insert_one(friend)

        return Response(response=json.dumps({"data": "Friend request sent", "success": True}), status=200, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Unauthorized as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="applcation/json")
    except Forbidden as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=403, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# delete friend request


@friend.route("/request/<username>", methods=["DELETE"])
def delete_friend_request(username):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        reciever_user = username

        dbResponse = db.friend_requests.delete_one(
            {"sender": user, "recipient": reciever_user})

        if dbResponse.deleted_count == 1:
            on_del_or_accept_friend_req(reciever_user, user)
            return Response(response=json.dumps({"data": "Friend request deleted", "success": True}), status=200, mimetype="application/json")
        else:
            return Response(response=json.dumps({"data": "No friend request was sent", "success": False}), status=200, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# accept friend


@friend.route("/accept/<username>", methods=["POST"])
def accept_friend_req(username):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        reciever_user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        user = username

        if user == reciever_user:
            raise Forbidden("Cannot add friend to yourself")

        inserted_response = db.friend.insert_one(
            {"user_1": username, "user_2": reciever_user})
        deleted_response = db.friend_requests.delete_one(
            {"sender": user, "recipient": reciever_user})

        if inserted_response.inserted_id is not None and deleted_response.deleted_count == 1:
            on_del_or_accept_friend_req(reciever_user, user)
            return Response(response=json.dumps({"data": "Friend added", "success": True}), status=200, mimetype="application/json")
        else:
            return Response(response=json.dumps({"data": "Something went wrong", "success": True}), status=400, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# Remove friend


@friend.route("/remove/<username>", methods=["DELETE"])
def remove_friend(username):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user_1 = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        user_2 = username

        dbResponse = db.friend.delete_one(
            {"$or": [{"user_1": user_1, "user_2": user_2}, {"user_1": user_2, "user_2": user_1}]})

        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"data": "Friend removed", "success": True}), status=200, mimetype="application/json")
        else:
            raise Exception("Something went wrong")

    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# GET FRIEND REQUESTS

@friend.route("/request", methods=["GET"])
def get_friend_request():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]

        friend_requests = list(db.friend_requests.find({"recipient": user}))
        for req in friend_requests:
            pfp = db.users.find_one({"username": req["sender"]})[
                "details"]["pfp"]
            req["sender_pfp"] = pfp
            del req["_id"]
        return Response(response=json.dumps({"data": friend_requests, "success": True}), status=200, mimetype="application/json")

    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")
