friend_req_send_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["sender", "recipient"],
        "properties": {
            "sender": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "recipient": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }
}

friend_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_1", "user_2"],
        "properties": {
            "user_1": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "user_2": {
                "bsonType": "string",
                "description": "must be a string  and is required",
            },
        }
    }
}
