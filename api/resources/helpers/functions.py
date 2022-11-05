import time
import calendar

# marketplace api and database will work along with the resources database, as the things on it
# will be the (mostly) paid resources such as notes / books

# resources database will contain the items, and tells wether paid or not.
# if they are paid, they appear in the marketplace
# clicking on it leads to buy page
# checkout will lead to payment using easypaisa and or other ways


class EmptyField(Exception):
    pass


def initialize_resource(content, username):

    gmt = time.gmtime()

    print(content)

    resource = {
        "username": username,
        "resource_title": content["resource_title"],
        "resource_type": content["resource_type"],
        "preview_image": content["preview_image"],
        "price": content["price"],
        "rating": content["rating"],
        "file_type": content["file_type"],
        # will be an array, single element in array in pdf, or else multiple links of images
        "subject": content["subject"],
        'link': content["link"],  # this will be a list
        "visibility": content["visibility"],
        "created": f"{calendar.timegm(gmt)}",
    }
    return resource


def check_content(content):
    if content["resource_title"] == "" or len(content["link"]) == 0:
        return EmptyField("Please dont leave any fields empty")
