from model.model import get_recommendations
import repository.articles as articles
import repository.users as users


def recommend(user_id, start=0, end=10):
    recommendations = get_recommendations(user_id, end)
    return articles.find_many(recommendations[start:end])


def get_user(user_id):
    """
    Get user by id
    """
    return users.find_one(user_id)


def get_random_user():
    """
    Get a random user
    """
    return users.find_random()
