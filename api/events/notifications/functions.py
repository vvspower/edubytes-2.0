import textwrap
import re
import sys
import os
from bson import ObjectId
from api import db_events, db
import datetime
import time
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))

try:
    from .models import notification_model
    db_events.create_collection("notifications")
    db_events.command("collMod", "users", validator=notification_model)
except Exception as ex:
    print(ex)


# HELPER
def create_notification(for_username, from_username, text, redirect, type="general"):
    presentDate = datetime.datetime.now()
    if from_username != "general":
        pfp = db.users.find_one({"username": from_username})["details"]["pfp"]
    else:
        pfp = "system"
    notification = {
        "for": for_username,
        "from": {"username": from_username, "pfp": pfp},
        "content": text,
        "created": f"{time.mktime(presentDate.timetuple())}",
        "read": False,
        "redirect": redirect,
        "details": {
            "type": type
        }
    }

    return notification


# FUNCTIONS
def on_create_user(username):
    text = "Congrats on making your account 🎉. Move on to your profile and add information 😊"
    redirect = f"/u/{username}"
    notification = create_notification(username, "general",  text, redirect)
    dbResponse = db_events.notifications.insert_one(notification)
    return dbResponse.inserted_id


def on_getting_reply(from_username, post_id, reply):

    text = f"{from_username} replied to your post: {textwrap.shorten(reply, width=15, placeholder='...')}"
    redirect = f'/post/{post_id}'
    for_username = db.forum.find_one({"_id": ObjectId(post_id)})["username"]
    notification = create_notification(
        for_username, from_username, text, redirect)
    dbResponse = db_events.notifications.insert_one(notification)


def on_being_mentioned(username_of_mentioner, post_id, content):
    mentioned_user = re.findall("@([a-zA-Z0-9]{1,15})", content)
    am = {}  # already mentioned
    for name in mentioned_user:
        am[name] = {}
        am[name]["mentioned"] = False

    text = f"{username_of_mentioner} mentioned you in a comment.."
    redirect = f'/post/{post_id}'
    for username in mentioned_user:
        # checks if user is mentioned more than 1 times. so notfication is only sent 1 time not the amount of times they were mentioned in the
        if am[username]["mentioned"] == True:
            continue
        if db.users.find_one({"username": username}) != None:
            notification = create_notification(
                username, username_of_mentioner, text, redirect)
            db_events.notifications.insert_one(notification)
            am[username]["mentioned"] = True

        else:
            continue
    for name in mentioned_user:
        am[name]["mentioned"] = False


def on_post_like(username, post_id, type):
    reaction = "reacted"
    if type == "like":
        reaction = "liked"
    # getting the username of the person whos post was liked
    for_username = db.forum.find_one({"_id": ObjectId(post_id)})["username"]
    text = f"{username} {reaction} your post "
    redirect = f"/post/{post_id}"
    notification = create_notification(
        for_username, username,  text, redirect, type=type)
    db_events.notifications.insert_one(notification)


# todo
# on friend request send


def on_sending_friend_request(for_username, from_username):
    text = f"{from_username} sent you a friend request"
    redirect = f"/u/{from_username}"
    notification = create_notification(
        for_username, from_username, text, redirect, type="friend_request")
    db_events.notifications.insert_one(notification)


def on_del_or_accept_friend_req(for_username, from_username):
    db_events.notifications.delete_one(
        {"for": for_username, "from.username": from_username, "details.type": "friend_request"})
