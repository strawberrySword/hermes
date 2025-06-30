from db import articles_collection, interactions_collection
from pymongo import IndexModel, ASCENDING, DESCENDING


def create_indexes():
    """
    Create indexes for the database collections
    """
    print("INDEXING")
    articles_collection.create_indexes([
        IndexModel([("date", DESCENDING)]),
        IndexModel([("topic", ASCENDING)])
    ])

    interactions_collection.create_indexes([
        IndexModel([("user", ASCENDING), ("last_recommended", DESCENDING)]),
        IndexModel([("user", ASCENDING), ("is_opened", ASCENDING)]),
        IndexModel([("user", ASCENDING), ("last_opened", DESCENDING)])
    ])
