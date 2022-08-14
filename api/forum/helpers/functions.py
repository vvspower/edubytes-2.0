import sys
import os
from api import db
from .exceptions import *

sys.path.append(os.path.abspath("../api"))
sys.path.append(os.path.abspath('../main'))


def content_check(content):
    if content["target"]:
        if content["content"] == "" or content["target"] == []:
            raise EmptyField("Please do not leave any field empty")
    if len(content["content"]) > 5000:
        raise StringTooLongException(
            "Content is too long. Please keep it below 5000 characters")
    if len(content["content"]) < 5:
        raise StringTooShortException(
            "Content is too short. Please keep it above 5 characters")


def add_likes(posts):
    for item in posts:
        likes = list(db.forum_likes.find({"post": str(item["_id"])}))
        print(likes)
        for like in likes:
            del like["_id"]
        item["likes"] = likes
    return posts
