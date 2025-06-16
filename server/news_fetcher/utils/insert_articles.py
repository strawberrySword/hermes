from db.mongo_client import collection
from pymongo.errors import DuplicateKeyError


def insert_article(article: dict):
    """
    Inserts a single article into the MongoDB 'articles' collection.
    Assumes the article has a unique 'url' field.
    """
    try:
        # Avoid duplicates by enforcing unique URL
        if collection.count_documents({"url": article["url"]}, limit=1) == 0:
            result = collection.insert_one(article)
            print(f"Inserted article '{article['title']}' with ID {result.inserted_id}")
        else:
            print(f"Skipped duplicate article: {article['title']}")
    except Exception as e:
        print(f"Error inserting article '{article['title']}': {e}")


def insert_articles(articles: list):
    """
    Inserts a list of articles into the collection, skipping duplicates.
    """
    for article in articles:
        insert_article(article)
