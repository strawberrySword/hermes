from db import articles_collection, likes_collection
from datetime import datetime


def find_many(ids):
    """
    Find many articles by their ids
    """
    return list(articles_collection.find({"article_id": {"$in": ids}}, {"_id": 0}))


def find_one(id):
    return articles_collection.find_one({"article_id": id}, {"_id": 0})


def get_seen(user_id, start=0, end=10):
    """
    Get seen articles for a user
    """
    articles = list(likes_collection.find({"user_id": user_id}, {
                    "article_id": 1, "_id": 0}).sort({"time_stamp": 1}).skip(start).limit(end))
    return [article["article_id"] for article in articles]


def get_liked(article_id, user_id):
    """
    Get liked article for a user
    """
    article = likes_collection.find_one(
        {"article_id": article_id, "user_id": user_id}, {"_id": 0})
    return article


def create_like(article_id, user_id):
    likes_collection.insert_one({
        'article_id': article_id,
        'user_id': user_id,
        'time_stamp': datetime.now()
    })


def delete_like(article_id, user_id):
    likes_collection.delete_many(
        {"user_id": user_id, "article_id": article_id})


def get_random(limit=10):
    """
    Get random articles
    """
    return list(articles_collection.aggregate([{"$sample": {"size": limit}}, {"$project": {"_id": 0}}]))
    # return articles_collection.find({}, {"_id": 0}).limit(limit)
