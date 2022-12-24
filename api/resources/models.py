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
            "preview_image": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "rating": {
                "bsonType": "number",
                "description": "must be a string and is required"
            },
            "raters": {
                "bsonType": "array",
                "description": "must be a array and is required"
            },
            "file_type": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "subject": {
                "bsonType": "subject",
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


# {
#   $jsonSchema: {
#     bsonType: 'object',
#     required: [
#       'username',
#       'resource_title',
#       'resource_type',
#       'preview_image',
#       'rating',
#       'subject',
#       'link',
#       'file_type',
#       'created'
#     ],
#     properties: {
#       username: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       resource_title: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       resource_type: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       preview_image: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       rating: {
#         bsonType: 'number',
#         description: 'must be a string and is required'
#       },
#       file_type: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       subject: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       },
#       link: {
#         bsonType: 'array',
#         description: 'must be a array and is required'
#       },
#       created: {
#         bsonType: 'string',
#         description: 'must be a string and is required'
#       }
#     }
#   }
# }
