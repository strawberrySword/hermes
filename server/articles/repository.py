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


def find_fresh(stale_articles):
    """
    Find fresh articles that are not stale.
    """
    now = datetime.now()
    stale_ids = [article['article_id'] for article in stale_articles]
    pipeline = [
        {"$match": {"_id": {"$nin": stale_ids}, "date": {"$lte": now}}},
        {"$addFields": {"id": {"$toString": "$_id"}}},
        {"$project": {"_id": 0}},
        {"$sort": {"date": -1}},
        {"$limit": 1000}
    ]
    return list(articles_collection.aggregate(pipeline))
