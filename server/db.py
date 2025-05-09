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
print("Connected to MongoDB")