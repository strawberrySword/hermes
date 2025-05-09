from db import user_collection


def find_one(id):
    """
    Find one user by their id
    """
    return user_collection.find_one({"user_id": id}, {"_id": 0})


def find_random():
    """
    Find a random user
    """
    return user_collection.aggregate([{"$sample": {"size": 1}}]).next()
