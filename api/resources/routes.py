from http.client import UNAUTHORIZED
from flask import Flask, Blueprint, request, Response
import json
from bson import ObjectId
import jwt
import sys
import os
from api import db, db_marketplace
from .helpers.functions import *
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

resources = Blueprint("resources", __name__)
JWT_SECRET_KEY = "d445191d82cd77c696de"


try:
    from .models import resource_model
    db_marketplace.create_collection("resources")
    db_marketplace.resources.create_index({"name": "text", "subject": "text"})
    db_marketplace.command("collMod", "resources", validator=resource_model)
    db_marketplace.create_collection("orders")
    # ? create collmod model
except Exception as ex:
    print(ex)


class EmptyField(Exception):
    pass


class Unauthorized(Exception):
    pass


# upload resource


@resources.route("/upload", methods=["POST"])
def upload_resource():
    try:
        content = request.get_json()
        check_content(content=content)
        # ? Check content function

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        resource = initialize_resource(
            content=content, username=user)
        db_response = db_marketplace.resources.insert_one(resource)
        return Response(response=json.dumps({"data": "uploaded"}), status=200, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


@resources.route("/<id>", methods=["PUT"])
def update_resources(id):
    try:
        content = request.get_json()
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        db_response = db.forum.update_one({"_id": ObjectId(id), "username": user["username"]}, {
            "$set": {"resource_title": content["resource_title"], "price": content["price"]}})
        if db_response.modified_count == 1:
            return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# delete resources


@resources.route("/<id>", methods=["DELETE"])
def delete_resource(id):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        if user["username"] == db_marketplace.resources.find_one({"_id": ObjectId(id)})["username"]:
            db_response = db_marketplace.resources.delete_one(
                {"_id": ObjectId(id)})
        else:
            raise Unauthorized("Unauthorized")

        if db_response.deleted_count == 1:
            return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
        else:
            raise Exception("Something went wrong")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get all resources


@resources.route("/", methods=["GET"])
def get_resources():
    try:
        resources = list(db_marketplace.resources.find())
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get specific resource


@resources.route("/<id>", methods=["GET"])
def get_specific_resource(id):
    try:
        resources = list(db_marketplace.resources.find({"_id": ObjectId(id)}))
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get free resource

@resources.route("/free", methods=["GET"])
def get_free_resource():
    try:
        resources = list(db_marketplace.resources.find({"price": 0}))
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")

# get paid resource


@resources.route("/paid", methods=["GET"])
def get_paid_resource():
    try:
        resources = list(db_marketplace.resources.find({"price": {"$ne": 0}}))
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get all user resources

@resources.route("/<username>", methods=["GET"])
def get_user_resource(username):
    try:
        resources = list(db_marketplace.resources.find({"username": username}))
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# search for query


@resources.route("/search/<query>", methods=["GET"])
def search_resource(query):
    try:
        resources = list(db_marketplace.resources.find(
            {"$text": {"$search": query}}))
        for item in resources:
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": "Something went wrong. Please try again"}), status=500, mimetype="application/json")
