from bson import ObjectId
from db import articles_collection
from datetime import datetime


def find_many(ids):
    """
    Find many articles by their ids
    """
    return list(articles_collection.find({"_id": {"$in": ids}}, {"_id": 0}))


def find_one(id):
    return articles_collection.find_one({"article_id": id}, {"_id": 0})


def get_random(limit=10):
    """
    Get random articles
    """
    return list(articles_collection.aggregate([{"$sample": {"size": limit}},
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
    pipeline = [
        {"$match": {
            "_id": {"$nin": stale_ids},
            "date": {"$lte": now},
        }},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$project": {"_id": 0}},
        {"$sort": {"date": -1}},
        {"$limit": 1000}
    ]
    if topic != "all":
        pipeline[0]["$match"]["topic"] = topic
    return list(articles_collection.aggregate(pipeline))


def get_top_topics(article_ids):
    """
    Get top topics from a list of article ids.
    """
    pipeline = [
        {"$match": {"_id": {"$in": article_ids}}},
        {"$group": {"_id": "$topic", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 6},
        {"$project": {"_id": 0, "topic": "$_id", "count": 1}}
    ]
    return list(articles_collection.aggregate(pipeline))
