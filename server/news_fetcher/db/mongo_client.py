from pymongo import MongoClient
import certifi


def print_article_count():
    count = collection.count_documents({})
    print(f"Total articles in local MongoDB: {count}")


MONGO_URI = "mongodb+srv://avivbaror:Test1234@newscollector.jsadksf.mongodb.net/?retryWrites=true&w=majority&appName=NewsCollector"
MONGO_L = "mongodb://localhost:27017"

client = MongoClient(MONGO_L)
db = client["news_db"]
collection = db["articles"]
print_article_count()
