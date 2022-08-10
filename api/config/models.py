user_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "password", "created", "details", "admin", "partnerd"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
                "uniqueItems": True
            },
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "password": {
                "bsonType": "binData",
                "description": "must be a bytes and is required"
            },
            "created": {
                "bsonType": "string",
                'description': "must be a string and is required",
            },
            "details": {
                "bsonType": "object",
                "description": "must be a object and is required",
            },
            "admin": {
                "bsonType": "bool",
                "description": "must be a object and is required",
            },
            "partnerd": {
                "bsonType": "bool",
                "description": "must be a object and is required",
            }
        }
    }
}

# FORUM

forum_post_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "content", "image", "created", "target", "subject", "tags"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "image": {
                "bsonType": "string",
                "description": "must be a bytes and is required"
            },
            "created": {
                "bsonType": "string",
                'description': "must be a string and is required",
            },
            "target": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "subject": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "tags": {
                "bsonType": "array",
                "description": "must be a array and is required",
            }
        }
    }
}

forum_reply_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "reply_to", "image", "content", "created"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "reply_to": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "image": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "created": {
                "bsonType": "string",
                'description': "must be a string and is required",
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required",
            }
        }
    }
}


# db.command("collMod", "users", validator=validator)
