from bson import ObjectId
from sympy import true
from db import interactions_collection, topic_interaction_collection, articles_collection
from datetime import datetime, timedelta


def record_open(user_email, article_id):
    now = datetime.now()

    interactions_collection.update_one(
        {"user": user_email, "article_id": article_id},
        {"$set": {"last_opened": now, "is_opened": True}},
        upsert=True
    )

    article = articles_collection.find_one({
        "_id": ObjectId(article_id)
    }, {"topic": 1})

    topic_interaction_collection.update_one(
        {"user": user_email, "topic": article["topic"]},
        {"$inc": {"count": 1}},
        upsert=True
    )


def record_recommended(user_id, article_id):
    now = datetime.now()
    interactions_collection.update_one(
        {"user": user_id, "article_id": article_id},
        {"$set": {"last_recommended": now}},
        upsert=True
    )


def get_user_interaction_data(user_id):
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    pipeline = [
        {"$match": {"user": user_id}},
        {
            "$facet": {
                "stale_articles": [
                    {
                        "$match": {
                            "$or": [
                                {"last_recommended": {"$gte": one_hour_ago}},
                                {"is_opened": True},
                            ]
                        }
                    },
                    {"$project": {"_id": 0, "article_id": 1}},
                ],
                "viewed_articles": [
                    {"$match": {"is_opened": True}},
                    {"$sort": {"last_opened": -1}},
                    {"$limit": 50},
                    {"$project": {"_id": 0, "article_id": 1}},
                ],
            }
        },
    ]
    result = list(interactions_collection.aggregate(pipeline))
    if not result:
        return {"stale_articles": [], "viewed_articles": []}
    return result[0]
