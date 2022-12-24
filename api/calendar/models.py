study_track_model = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "title", "description" "due_date", "attatchments", "created"],
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
                "bsonType": "boolean",
                "description": "must be a string and is required",
            },
            "attatchments": {
                "bsonType": "array",
                "description": "must be a array and is required",
            },
            "created": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }
}

# CREATE, UPDATE , DELETE
