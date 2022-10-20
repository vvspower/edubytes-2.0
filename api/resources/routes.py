from crypt import methods
import resource
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
    db_marketplace.command("collMod", "resources", validator=resource_model)
    db_marketplace.create_collection("orders")
    # ? create collmod model
except Exception as ex:
    print(ex)


@resources.route("/upload", methods=["POST"])
def upload_resource():
    try:
        content = request.get_json()
        # ? Check content function

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})[
            "username"]
        resource = initialize_resource(
            content=content, username=user["username"])
        db_response = db_marketplace.resources.insert_one(resource)
        return Response(response=json.dumps({"data": resource}), status=200, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    # except StringTooShortException as ex:
    #     return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    # except StringTooLongException as ex:
    #     return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    # except EmptyField as ex:
    #     return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0]}), status=500, mimetype="application/json")
