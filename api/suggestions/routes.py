
from flask import Flask, Blueprint, Response
from .suggestions_config import *
import json

suggestions = Blueprint('suggestions', __name__)


@suggestions.route("/from_post/<id>", methods=["GET"])
def get_suggestion_post(id):
    try:
        posts = get_suggested_posts_according_to_post(id)

        return Response(response=json.dumps({"data": posts, "success": True}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


@suggestions.route("/from_user/<username>")
def get_suggestion_user(username):
    try:
        suggested_users = get_suggested_users_using_education(username)
        return Response(response=json.dumps({"data": suggested_users, "success": True}), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")
