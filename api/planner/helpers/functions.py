import sys
import os
from api import db
import calendar
import time

#  "username": {
#             "bsonType": "string",
#             "description": "must be a string and is required",
#         },
#         "title": {
#             "bsonType": "string",
#             "description": "must be a string and is required",
#         },
#         "description": {
#             "bsonType": "string",
#             "description": "must be a string and is required",
#         },
#         "due_date": {
#             "bsonType": "string",
#             "description": "must be a string and is required",
#         },
#         "completed": {
#             "bsonType": "bool",
#             "description": "must be a boolean and is required",
#         },
#         "type": {
#             "bsonType": "string",
#             "description": "must be a string and is required",
#         },
#         # type = exam / study
#         "attatchments": {
#             "bsonType": "array",
#             "description": "must be a array and is required",
#         },
#         "created": {
#             "bsonType": "string",
#             "description": "must be a string and is required"
#         }


def initialize_planner(content, user):
    gmt = time.gmtime()
    planner = {
        "username": user["username"],
        "title": content["title"],
        "description": content["description"],
        "due_date": content["due_date"],
        "completed": content["completed"],
        "type": content["type"],
        "attatchments": content["attatchments"],
        "created": f"{calendar.timegm(gmt)}"
    }
    return planner
