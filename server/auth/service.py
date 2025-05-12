import auth.repository as users


def get_user(user_id: str):
    """
    Get user by id
    """
    return users.find_one(user_id)


def get_random_user():
    """
    Get a random user
    """
    return users.find_random()
