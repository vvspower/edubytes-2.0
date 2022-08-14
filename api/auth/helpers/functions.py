import os
import sys
from api import db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .exceptions import *
import datetime
import time
sys.path.append(os.path.abspath("../../api"))
sys.path.append(os.path.abspath('../../main'))


EMAIL = "business.valpal@gmail.com"
APP_PASSWORD = "gosbnnqaciwliteg"

# SEND EMAIL


def send_email(email, token):

    message = MIMEMultipart()
    message["from"] = "ValPal"
    message["to"] = email
    message["subject"] = "Email Verification"

    message.attach(MIMEText(f"""
Hi {email},

We recieved your request for creating an account

please click on this link to verfiy your account (link of website)  {token}

Code will expire after 15 minutes

Thanks,
EduBytes""", 'plain'))

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(message)
        print("Sent")


def check_email_exists(email):
    dbResponse = db.users.find_one({"email": email})
    if dbResponse != None:
        raise RequiredExists("email already exists")


def check_username_exists(username):
    dbResponse = db.users.find_one({"username": username})
    if dbResponse != None:
        raise RequiredExists("username already exists")


def initialize_user(payload):
    presentDate = datetime.datetime.now()
    user = {
        "username": payload["username"],
        "email": payload["email"],
        "password": payload["password"].encode('utf-8'),
        "created": f"{time.mktime(presentDate.timetuple())}",
        "admin": False,
        "partnerd": False,
        "details": {
            "bio": None,
            "pfp": None,
            "verified": False
        },
        "education": {
            "institute": None,  # string
            "university": None,  # bool
            "college": None,  # bool,
            "subjects": [],  # array of strings
        }
    }

    return user


def get_friends(username):
    friends = list(db.friend.find(
        {"$or": [{"user_1": username}, {"user_2": username}]}))

    all_friends = []

    for friend in friends:
        del friend["_id"]
        for key, value in friend.items():
            if value != username:
                friend_name = value
        pfp = db.users.find_one({"username": friend_name})["details"]["pfp"]
        all_friends.append({"username": friend_name, "pfp": pfp})

    print(friends)

    return all_friends
