# connect to mongoDB
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["hermes"]
user_collection = db["users"]
articles_collection = db["articles"]
interactions_collection = db["interactions"]
topic_interaction_collection = db["topic_interactions"]
print("Connected to MongoDB")
