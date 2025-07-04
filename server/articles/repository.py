from bson import ObjectId
from db import articles_collection, topic_interaction_collection
from datetime import datetime


def find_many(ids):
    """
    Find many articles by their ids
    """
    return list(articles_collection.find({"_id": {"$in": ids}}, {"_id": 0, "embeddings": 0}))


def find_one(id):
    return articles_collection.find_one({"article_id": id}, {"_id": 0, "embeddings": 0})


def get_random(limit=10):
    """
    Get random articles
    """
    now = datetime.now()
    return list(articles_collection.aggregate([{"$match": {"date": {"$lte": now}}}, {"$sample": {"size": limit}},
                                               {"$addFields": {
                                                   "id": {"$toString": "$_id"}
                                               }
    },
        {"$project": {"_id": 0}}]))


def find_fresh(stale_articles, topic):
    """
    Find fresh articles that are not stale.
    """
    now = datetime.now()
    stale_ids = [ObjectId(article['article_id']) for article in stale_articles]
    limit = 1000 if topic == "all" else 1000
    pipeline = [
        {"$match": {
            "_id": {"$nin": stale_ids},
            "date": {"$lte": now},
        }},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$project": {"_id": 0}},
        {"$sort": {"date": -1}},
        {"$limit": limit}
    ]
    if topic != "all":
        pipeline[0]["$match"]["topic"] = topic
    return list(articles_collection.aggregate(pipeline))


def get_top_topics(user_email):
    """
    Get top topics from a list of article ids.
    """
    top_topics = topic_interaction_collection.find(
        {"user": user_email}, {"_id": 0, "embeddings": 0}).sort({"count": -1}).limit(6)
    return list(top_topics)
