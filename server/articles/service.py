from model.model import get_recommendations
import articles.repository as repository


def recommend(user_id, start=0, end=10):
    recommendations = get_recommendations(user_id, end)
    return repository.find_many(recommendations[start:end])


def get_seen(user_id, start=0, end=10):
    seen = repository.get_seen(user_id, start, end)
    return repository.find_many(seen)


def get_liked(article_id, user_id):
    article = repository.get_liked(article_id, user_id)
    return article


def like_article(article_id, user_id):
    article = repository.find_one(article_id)
    if not article:
        return None

    repository.create_like(article_id, user_id)
    return article


def delete_like(article_id, user_id):
    repository.delete_like(article_id, user_id)
