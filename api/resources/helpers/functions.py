# marketplace api and database will work along with the resources database, as the things on it
# will be the (mostly) paid resources such as notes / books

# resources database will contain the items, and tells wether paid or not.
# if they are paid, they appear in the marketplace
# clicking on it leads to buy page
# checkout will lead to payment using easypaisa and or other ways

def initialize_resource(content, username):
    resource = {
        "username": username,
        "resource_title": content["resource_title"],
        "resource_type": content["resource_type"],
        "price": content["price"],
        "rating": content["rating"],
        "file_type": content["file_type"],
        "created": content["created"],
        "resource_title": content["resource_title"]
    }
    return resource
