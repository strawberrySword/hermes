from flask import jsonify
import interactions.repository as repository


def record_opened(user_email, article_id):
    """
    Handle the interaction with an article by the user.
    """
    repository.record_open(user_email, article_id)


def record_recommended(user_id, article_id):
    """
    Handle the recommendation interaction with an article by the user.
    """
    repository.record_recommended(user_id, article_id)


def record_many_recommended(user_id, article_ids):
    """
    Handle the recommendation interaction with multiple articles by the user.
    """
    for article_id in article_ids:
        repository.record_recommended(user_id, article_id)


def get_stale(user_id):
    """
    Get the interaction state for a specific article by the user.
    """
    return jsonify(repository.get_stale(user_id))


def get_viewed(user_id):
    """
    Get the viewed articles for the user.
    """
    return jsonify(repository.get_viewed(user_id))
