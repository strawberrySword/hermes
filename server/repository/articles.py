from db import articles_collection


def find_many(ids):
    """
    Find many articles by their ids
    """
    return list(articles_collection.find({"article_id": {"$in": ids}}, {"_id": 0}))
