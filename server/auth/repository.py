from db import user_collection


def find_one(id: str):
    """
    Find one user by their id
    """
    return user_collection.find_one({"user_id": id}, {"_id": 0})


def find_random():
    """
    Find a random user
    """
    return user_collection.aggregate([
        {"$sample": {"size": 1}},
        {"$project": {"_id": 0}}
    ]).next()


def find_by_email(email: str):
    """
    Find a user by their email
    """
    return user_collection.find_one({"email": email}, {"_id": 0})


def create_user(user_data: dict):
    """
    Create a new user
    """
    user_collection.insert_one(user_data)
    print(f"User created: {user_data.get('email', 'Unknown Email')}")


def upsert_one(user_data: dict):
    user_collection.update_one(
        {'email': user_data["email"]},
        {'$setOnInsert':
            user_data
         },
        upsert=True
    )
