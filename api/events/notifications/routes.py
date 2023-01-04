
from flask import Flask, Blueprint, request, Response
import sys
import os
from bson import ObjectId
import jwt
import json
from api import db_events, db
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

notification = Blueprint('notification', __name__)
JWT_SECRET_KEY = "d445191d82cd77c696de"


@notification.route("", methods=["GET"])
def get_notifications():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})
        notifs = list(db_events.notifications.find(
            {"for": user["username"]}).limit(12))
        for notif in notifs:
            notif["_id"] = str(notif["_id"])
        dbResponse = db_events.notifications.update_many({"for": user["username"]}, {
            "$set": {"read": True}})

        notifs.reverse()
        return Response(response=json.dumps({"data": notifs, "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


@notification.route("/latest", methods=["GET"])
def get_latest_notifications():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})
        notifs = list(db_events.notifications.find(
            {"for": user["username"], "read": False}))
        for notif in notifs:
            notif["_id"] = str(notif["_id"])
        dbResponse = db_events.notifications.update_many({"for": user["username"]}, {
            "$set": {"read": True}})
        return Response(response=json.dumps({"data": notifs, "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")
