user_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "email", "password", "created", "details", "education", "admin", "partnerd"],
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
            "education": {
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


notification_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["for", "content", "created", "redirect"],
        "properties": {
            "for": {
                "bsonType": "string",
                "description": "must be a string and is required",
                "uniqueItems": True
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "created": {
                "bsonType": "string",
                'description': "must be a string and is required",
            },
            "redirect": {
                "bsonType": "string",
                "description": "must be a string and is required",

            }
        }
    }
}
