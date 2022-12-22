import json
import os
import sys
from http.client import UNAUTHORIZED

import jwt
from bson import ObjectId
from flask import Blueprint, Flask, Response, request

from api import db, db_marketplace

from .helpers.functions import *

sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

resources = Blueprint("resources", __name__)
JWT_SECRET_KEY = "d445191d82cd77c696de"


try:
    from .models import resource_model
    db_marketplace.create_collection("resources")
    db_marketplace.create_collection("resource_rating")
    ok = db_marketplace.resources.create_index({"resource_title": "text"})
    print(ok)
    # db_marketplace.command("collMod", "resources", validator=resource_model)
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
        user_pfp = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "details"]["pfp"]

        resource = initialize_resource(
            content=content, username=user, pfp=user_pfp)
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
        if user == db_marketplace.resources.find_one({"_id": ObjectId(id)})["username"]:
            db_response = db_marketplace.resources.delete_one(
                {"_id": ObjectId(id)})
        else:
            raise Unauthorized("Unauthorized")

        if db_response.deleted_count == 1:
            return Response(response=json.dumps({"data": "deleted successfully"}), status=200, mimetype="application/json")
        else:
            raise Exception("Something went wrong")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get all resources


@resources.route("/", methods=["GET"])
def get_resources():
    try:
        resources = list(db_marketplace.resources.find(
            {"visibility": "public"}))
        for item in resources:
            item["_id"] = str(item["_id"])
            item["rating"] = get_resource_rating(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get specific resource


@resources.route("/<id>", methods=["GET"])
def get_specific_resource(id):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        username = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        resources = db_marketplace.resources.find_one({"_id": ObjectId(id)})
        resources["_id"] = str(resources["_id"])
        resources["rating"] = get_resource_rating(
            resources["_id"])
        print("here")
        rating = db_marketplace.resource_rating.find_one(
            {"username": username, "resource_id": id})
        print("--------")
        print(rating)
        print("--------")

        if rating == None:
            resources["user_rated"] = 0
        else:
            resources["user_rated"] = rating["rating"]
        print(resources)

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get free resource


# get all user resources

@resources.route("/<username>", methods=["GET"])
def get_user_resource_public(username):
    try:
        resources = list(db_marketplace.resources.find(
            {"username": username, "visibility": "public"}))
        for item in resources:
            item["_id"] = str(item["_id"])
            item["rating"] = get_resource_rating(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# get user resources with auth

@resources.route("/user", methods=["GET"])
def get_user_resource_private():
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        username = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        resources = list(db_marketplace.resources.find(
            {"username": username}))
        for item in resources:
            item["_id"] = str(item["_id"])
            item["rating"] = get_resource_rating(item["_id"])

        return Response(response=json.dumps({"data": resources}), status=200, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")


# search for query

# conditions

# all boards - search
# 1 board - all subjects - search
# 1 board - 1 subject - search


@resources.route("/search/<board>/<subject>/<query>", methods=["GET"])
def search_resource(board, subject, query):
    try:
        return_resource = []
        if board == "all":
            if query == "all":
                return_resource = list(
                    db_marketplace.resources.find({"visibility": "public"}))
            else:
                return_resource = list(db_marketplace.resources.find(
                    {"$text": {"$search": query}, "visibility": "public"}))

        if board != "all" and subject == "all":
            if query != "all":
                return_resource = list(db_marketplace.resources.find(
                    {"$text": {"$search": query}, "board": board, "visibility": "public"}))
            else:
                return_resource = list(db_marketplace.resources.find(
                    {"board": board, "visibility": "public"}))

        if board != "all" and subject != "all":
            if query != "all":
                return_resource = list(db_marketplace.resources.find(
                    {"$text": {"$search": query}, "board": board, "subject": subject, "visibility": "public"}))
            else:
                return_resource = list(db_marketplace.resources.find(
                    {"board": board, "subject": subject, "visibility": "public"}))
        # todo: create ability to also search when selected filters of all
        for item in return_resource:
            item["_id"] = str(item["_id"])
            item["rating"] = get_resource_rating(item["_id"])

        return Response(response=json.dumps({"data": return_resource}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": "Something went wrong. Please try again"}), status=500, mimetype="application/json")

# updating rating


@resources.route("/rating/<id>", methods=["PUT"])
def create_rating(id):
    try:
        content = request.get_json()
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        username = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        user_rating = db_marketplace.resource_rating.find_one(
            {"username": username, "resource_id": id})

        print(user_rating)
        if user_rating != None:
            db_marketplace.resource_rating.update_one(
                {"resource_id": id, "username": username}, {"$set": {"rating": int(content["rating"])}})
        if user_rating == None:
            db_marketplace.resource_rating.insert_one(
                {"resource_id": id, "username": username, "rating": int(content["rating"])})

        return Response(response=json.dumps({"data": content["rating"]}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": "Something went wrong. Please try again"}), status=500, mimetype="application/json")
