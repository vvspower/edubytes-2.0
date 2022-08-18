notification_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["for", "from" "content", "created", "redirect", "details"],
        "properties": {
            "for": {
                "bsonType": "object",
                "description": "must be a string and is required",
            },
            "from": {
                "bsonType": "object",
                "description": "must be a string and is required",
            },
            "content": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "created": {
                "bsonType": "string",
                'description': "must be a string and is required",
            },
            "read": {
                "bsonType": "bool",
                'description': "must be a bool and is required",
            },
            "redirect": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "details": {
                "bsonType": "string",
                "description": "must be a string and is required",
            }

        }
    }
}
