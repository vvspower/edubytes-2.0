study_track_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "title", "description" "due_date", "completed", "type",  "attatchments", "created"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "title": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "description": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "due_date": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "completed": {
                "bsonType": "bool",
                "description": "must be a boolean and is required",
            },
            "type": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            # type = exam / study
            "attatchments": {
                "bsonType": "object",
                "description": "must be a object and is required",
            },
            "created": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }

        }
    }
}

# CREATE, UPDATE , DELETE
