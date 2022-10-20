# resourses new database folder
# ability to upload / delete resources using google drive api

resource_model = {
    "$jsonSchema": {
        "bsonType": "object",
        # type = PDF / Images
        "required": ["username", "resource_title", "resource_type" "price", "rating", "file_type"  "created"],
        # if price is 0 then free
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "resource_title": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "resource_type": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "price": {
                "bsonType": "number",
                "description": "must be a string and is required"
            },
            "rating": {
                "bsonType": "number",
                "description": "must be a string and is required"
            },
            "file_type": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "link": {
                "bsonType": "array",
                "description": "must be a array and is required"
            },
            "created": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }
}
