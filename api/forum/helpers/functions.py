import sys
import os
from api import db
from .exceptions import *
import calendar
import time

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


def sort_posts_by_likes(post):
    sorted_post = sorted(post, key=lambda d: len(d["likes"]), reverse=True)[:2]
    return sorted_post


def filter_between_today_and_24h_ago(posts):
    gmt = time.gmtime()
    return list(filter(lambda item: int(
        item["created"]) > calendar.timegm(gmt), posts))


def filter_between_24h_ago_and_before(posts):
    gmt = time.gmtime()
    return list(filter(lambda item: int(
        item["created"]) > calendar.timegm(gmt), posts))


def calculate_case(today_posts, yesterday_posts, case):
    return_list = []
    if len(today_posts) == 1:
        case = "both"
        return_list.append(today_posts[0])
        return_list.append(yesterday_posts[0])
    if len(today_posts) == 0:
        case = "yesterday"
        return_list = yesterday_posts
    else:
        return_list = today_posts
    for item in return_list:
        item["_id"] = str(item["_id"])
        print("HELLO")

    return return_list, case
