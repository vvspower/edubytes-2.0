from ast import excepthandler
from http.client import UNAUTHORIZED
from ..events.notifications.functions import on_being_mentioned, on_getting_reply, on_post_like
from re import L
from telnetlib import EC
from xml.dom import NotFoundErr
from flask import Flask, Blueprint, request, Response
from bson import ObjectId
import json
import datetime
import time
import sys
import os
from api import db
import jwt
from .helpers.exceptions import *
from .helpers.functions import *
import calendar
import time
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))


forum = Blueprint('forum', __name__)
JWT_SECRET_KEY = "d445191d82cd77c696de"


# HELPER


try:
    from .models import forum_post_model, forum_reply_model

    db.create_collection('forum')
    db.create_collection('forum_replies')
    db.create_collection('forum_likes')
    db.command("collMod", "forum", validator=forum_post_model)
    db.command("collMod", "forum_replies", validator=forum_reply_model)


except Exception as ex:
    print(ex)


# CREATE POST


@forum.route("/post", methods=["POST"])
def post():
    try:
        content = request.get_json()
        content_check(content)

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        gmt = time.gmtime()

        data = {
            "username": user["username"],
            "content": content["content"],
            "image": content["image"],
            "created": f"{calendar.timegm(gmt)}",
            "target": content["target"],  # target = "IBA"
            # subject = "Computer Science" or could by "General" for general subject
            "subject": content["subject"],
            "tags": content["tags"],
        }

        dbResponse = db.forum.insert_one(data)

        on_being_mentioned(
            user["username"], dbResponse.inserted_id, content["content"])
        return Response(response=json.dumps({"data": str(dbResponse.inserted_id), "success": True}), status=200, mimetype="application/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except StringTooShortException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except StringTooLongException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# UPDATE POST


@forum.route("/post/<id>", methods=["PUT"])
def update_post(id):
    try:
        content = request.get_json()
        content_check(content)

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        dbResponse = db.forum.update_one({"_id": ObjectId(id), "username": user["username"]}, {
                                         "$set": {"content": content["content"], "image": content["image"]}})

        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"data": "Updated", "success": True}), status=200, mimetype="applcation/json")
        else:
            return Response(response=json.dumps({"data": "Nothing to update", "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except StringTooShortException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except StringTooLongException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# DELETE POST


@forum.route("/post/<id>", methods=["DELETE"])
def delete_post(id):
    try:
        content = request.get_json()
        content_check(content)

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        post = db.forum.find_one({"_id": ObjectId(id)})
        if post["username"] == user["username"]:
            dbResponse = db.forum.delete_one({"_id": ObjectId(id)})
        else:
            return Response(response=json.dumps({"data": "Unauthorized", "success": False}), status=401, mimetype="applcation/json")

        if dbResponse.deleted_count == 1:
            return Response(response=json.dumps({"data": "Deleted", "success": True}), status=200, mimetype="applcation/json")
        else:
            raise Exception("Something went wrong")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except StringTooShortException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except StringTooLongException as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except EmptyField as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# GET SPECIFIC POST


@forum.route("/post/<id>", methods=["GET"])
def get_post(id):
    try:
        post = db.forum.find_one({"_id": ObjectId(id)})
        if post == None:
            raise NotFoundErr("Post not found")
        user = db.users.find_one({"username": post["username"]})
        likes = list(db.forum_likes.find({"post": id}))
        for item in likes:
            item["user_pfp"] = db.users.find_one({"username": item["username"]})[
                "details"]["pfp"]
            del item["_id"]
        post["likes"] = likes
        post["user_pfp"] = user["details"]["pfp"]
        post["_id"] = str(post["_id"])
        return Response(response=json.dumps({"data": post, "success": True}), status=200, mimetype="applcation/json")

    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")


# Posts by target and subject


@forum.route("/post/i/<target>/<subject>", methods=["GET"])
def get_posts_from_target(target, subject):
    try:
        posts = list(db.forum.find({"target": target, "subject": subject}))

        for item in posts:
            user = db.users.find_one({"username": item["username"]})
            item["user_pfp"] = user["details"]["pfp"]
            item["_id"] = str(item["_id"])
            likes = list(db.forum_likes.find({"post": str(item["_id"])}))
            for like in likes:
                like["user_pfp"] = db.users.find_one({"username": like["username"]})[
                    "details"]["pfp"]
                del like["_id"]
                del like["post"]
            item["likes"] = likes
        sorted_post = sorted(posts, key=lambda d: d["created"], reverse=True)
        return Response(response=json.dumps({"data": sorted_post, "success": True}), status=200, mimetype="applcation/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# Posts from specific user


@forum.route("/post/user/<username>", methods=["GET"])
def get_post_from_username(username):
    try:
        posts = list(db.forum.find({"username": username}))
        if posts == None:
            raise NotFoundErr("user does not exist")
        for item in posts:
            user = db.users.find_one({"username": item["username"]})
            print(str(item["_id"]))
            likes = list(db.forum_likes.find({"post": str(item["_id"])}))
            for like in likes:
                del like["_id"]
                del like["post"]
                like["user_pfp"] = db.users.find_one({"username": like["username"]})[
                    "details"]["pfp"]

            print(likes)
            item["likes"] = likes
            item["user_pfp"] = user["details"]["pfp"]
            item["_id"] = str(item["_id"])
            posts = sort_posts_by_date(posts)
        return Response(response=json.dumps({"data": posts, "success": True}), status=200, mimetype="applcation/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# GET TOP POSTS

@forum.route("/post/top/<target>", methods=["GET"])
def get_top_posts(target):
    try:
        case = "today"
        return_list = []
        posts = list(db.forum.find({"target": target}))
        posts = add_likes(posts)
        print("start")

        # finds posts which were created between today and 24 hours ago

        filtered_today = filter_between_today_and_24h_ago(posts)
        print(filtered_today)
        # finds posts which were created 24 hours ago and before
        filtered_yesterday = filter_between_24h_ago_and_before(posts)

        filtered_today = sort_posts_by_likes(filtered_today)
        filtered_yesterday = sort_posts_by_likes(filtered_yesterday)

        # calculated case
        return_list, case = calculate_case(
            filtered_today, filtered_yesterday, case)

        for item in return_list:
            for user in item["likes"]:
                del user["post"]
                user["user_pfp"] = db.users.find_one({"username": user["username"]})[
                    "details"]["pfp"]
                pass

            pfp = db.users.find_one({"username": item["username"]})[
                "details"]["pfp"]

            print(pfp)
            item["user_pfp"] = pfp

        print(return_list)
        return Response(response=json.dumps({"data": {"case": case, "sorted": return_list}, "success": True}), status=200, mimetype="applcation/json")

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")

# FILTER TAGS


@forum.route("/post/filter/<target>/<tag>", methods=["GET"])
def filter_post_using_tags(target, tag):
    try:
        posts = list(db.forum.find(
            {"tags": {"$all": [tag]}, "target": target}))
        for post in posts:
            post["_id"] = str(post["_id"])
        print(posts)
        return Response(response=json.dumps({"data": posts, "success": True}), status=200, mimetype="applcation/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# ? LIKE API


@forum.route("/post/like/<id>/<type>", methods=["POST"])
def like_post(id, type):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        if db.forum.find_one({"_id": ObjectId(id)}) == None:
            raise NotFoundErr("Post does not exist")
        if db.forum_likes.find_one({"username": user["username"], "post": id}) != None:
            raise Forbidden("Already liked")

        data = {
            "username": user["username"],
            "post": id,
            "type": type  # haha, sad, angry
        }

        if user["username"] != db.forum.find_one({"_id": ObjectId(id)})["username"]:
            on_post_like(user["username"], id, type)

        dbResponse = db.forum_likes.insert_one(data)
        return Response(response=json.dumps({"data": "Liked", "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except Forbidden as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=403, mimetype="application/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


@forum.route("/post/like/<id>", methods=["DELETE"])
def unlike_post(id):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        if db.forum.find_one({"_id": ObjectId(id)}) == None:
            raise NotFoundErr("Post does not exist")

        dbResponse = db.forum_likes.delete_one(
            {"username": user["username"], "post": id})

        return Response(response=json.dumps({"data": "unLiked", "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")

# put this in get posts

# TODO : remove if not needed


@forum.route("/post/like/<id>", methods=["GET"])
def check_if_liked_post(id):
    try:
        liked = False
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        if db.forum.find_one({"_id": ObjectId(id)}) == None:
            raise NotFoundErr("Post does not exist")

        dbResponse = db.forum_likes.find_one(
            {"username": user["username"], "post": id})
        if dbResponse != None:
            liked = True

        return Response(response=json.dumps({"data": liked, "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# TODO


# ? REPLIES


# Create Reply

@forum.route("/reply/<id>", methods=["POST"])
def reply_to_post(id):
    try:
        content = request.get_json()
        # content_check(content)

        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        if db.forum.find_one({"_id": ObjectId(id)}) == None:
            raise NotFoundErr("Post not found")

        gmt = time.gmtime()

        data = {
            "username": user["username"],
            "reply_to": id,
            "image": content["image"],
            "content": content["content"],
            "created": f"{calendar.timegm(gmt)}"
        }

        dbResponse = db.forum_replies.insert_one(data)
        on_getting_reply(user["username"], id, content["content"])
        on_being_mentioned(user["username"], id, content["content"])

        return_data = data
        return_data["_id"] = str(dbResponse.inserted_id)
        return_data["user_pfp"] = user["details"]["pfp"]

        return Response(response=json.dumps({"data": return_data, "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# Delete Reply

@forum.route("/reply/<id>", methods=["DELETE"])
def delete_reply_to_post(id):
    try:
        token = request.headers['Authorization']
        payload = jwt.decode(
            jwt=token,  key=JWT_SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({"_id": ObjectId(payload["user_id"])})

        dbResponse = db.forum_replies.delete_one(
            {"_id": ObjectId(id), "username": user["username"]})
        if dbResponse.deleted_count == 0:
            raise Unauthorized("Not Allowed")

        return Response(response=json.dumps({"data": "Deleted", "success": True}), status=200, mimetype="applcation/json")
    except jwt.exceptions.DecodeError as ex:
        return Response(response=json.dumps({"data": "Please use a valid form of JWT token", "success": False}), status=400, mimetype="applcation/json")
    except jwt.InvalidSignatureError as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=400, mimetype="application/json")
    except NotFoundErr as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=404, mimetype="application/json")
    except Unauthorized as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=403, mimetype="application/json")
    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")


# Get Replies

@forum.route("/reply/<id>", methods=["GET"])
def get_replies_to_post(id):
    try:
        posts = list(db.forum_replies.find({"reply_to": id}))
        for item in posts:
            item["user_pfp"] = db.users.find_one({"username": item["username"]})[
                "details"]["pfp"]
            item["_id"] = str(item["_id"])

        return Response(response=json.dumps({"data": posts, "success": True}), status=200, mimetype="applcation/json")

    except Exception as ex:
        return Response(response=json.dumps({"data": ex.args[0], "success": False}), status=500, mimetype="application/json")
