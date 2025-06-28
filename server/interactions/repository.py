from db import articles_collection, interactions_collection
from datetime import datetime


def record_open(user_email, article_id):
    now = datetime.now()

    interactions_collection.update_one(
        {"user": user_email, "article_id": article_id},
        {"$set": {"last_opened": now, "is_opened": True}},
        upsert=True
    )


def record_recommended(user_id, article_id):
    now = datetime.now()
    print(f"Recording recommendation for user {user_id} and article {article_id} at {now}")
    interactions_collection.update_one(
        {"user": user_id, "article_id": article_id},
        {"$set": {"last_recommended": now}},
        upsert=True
    )


def get_stale(user_id):
    one_hour_ago = datetime.now().timestamp() - 3600

    return list(interactions_collection.find({
        "user": user_id,
        "$or": [
            {"last_recommended": {"$gte": one_hour_ago}},
            {"is_opened": True}
        ]
    },
        {"_id": 0, "article_id": 1}))


def get_viewed(user_id):
    return list(interactions_collection.find(
        {"user": user_id, "is_opened": True},
        {"_id": 0, "article_id": 1}
    ).sort("last_opened", -1).limit(100))
