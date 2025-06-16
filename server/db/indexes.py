from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING
import os


def create_indexes():
    """
    Create indexes for the database collections
    """
    # Create indexes for likes_collection
    # likes_collection.create_index(
    # [("user_id", ASCENDING)], name="user_id_index")
    likes_collection.create_indexes([
        IndexModel([("user_id", ASCENDING), ("article_id", ASCENDING)]),
        IndexModel([("article_id", ASCENDING), ("user_id", ASCENDING)])
    ])


if __name__ == "__main__":
    # Create indexes
    load_dotenv()

    MONGO_URL = os.getenv("MONGO_URL")

    client = MongoClient(MONGO_URL)
    db = client["hermes"]
    user_collection = db["users"]
    articles_collection = db["articles"]
    likes_collection = db["likes"]
    create_indexes()
