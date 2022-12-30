from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from flask import Blueprint, request, Response
from .helpers.functions import *
from magic import from_buffer
from werkzeug.datastructures import FileStorage
import requests
import sys
import os
import json


import jwt
from bson import ObjectId
from api import db
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))


JWT_SECRET_KEY = "d445191d82cd77c696de"
planner = Blueprint("planner", __name__)

try:
    from .models import study_track_model
    db.create_collection("planner")
    db.command("collMod", "planner", validator=study_track_model)

except Exception as ex:
    print(ex)


def upload_file(files):
    print(files)
    file_urls = []
    for file in files:
        response = requests.post("https://script.google.com/macros/s/AKfycbzV9a3N1hN-5BZOgA8ngiQXXflR2o9gLgKgofK5gLAtmlcWvEGgirpSnk2Lo3rmjL70ug/exec", {"file": {
            "data": file,
            "name": file.filename,
            "type": from_buffer(file.read(), mime=True)
        }})
        print(response)

    pass


# create planner

@planner.route("/", methods=["POST"])
def create_planner():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        content = request.get_json()
        planner = initialize_planner(content, user)
        response = db.planner.insert_one(planner)
        planner["_id"] = str(response.inserted_id)
        return Response(response=json.dumps({"data": planner, "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# get planners


@planner.route("/", methods=["GET"])
def get_planner():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})
        response = list(db.planner.find({"username": user["username"]}))
        for item in response:
            item["_id"] = str(item["_id"])
        return Response(response=json.dumps({"data": response, "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")

# update


@planner.route("/<id>", methods=["PUT"])
def update_planner(id):
    try:
        content = request.get_json()
        print(content)
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})
        response = db.planner.update_one({"_id": ObjectId(id), "username": user["username"]}, {
            "$set": {"title": content["title"], "description":  content["description"], "due_date": content["due_date"], "attatchments": content["attatchments"]}})
        return Response(response=json.dumps({"data": "updated", "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# delete


@planner.route("/<id>", methods=["DELETE"])
def delete_planner(id):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})
        response = db.planner.delete_one(
            {"_id": ObjectId(id), "username": user["username"]})
        return Response(response=json.dumps({"data": "deleted", "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")
