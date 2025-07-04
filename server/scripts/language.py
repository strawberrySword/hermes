import pymongo
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from tqdm import tqdm

# Ensure reproducibility
DetectorFactory.seed = 0

# 1. Establish connection to MongoDB
# Replace the URI with your MongoDB connection string
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient(MONGO_URI)

db = client['hermes']
collection = db['articles']

# 2. Function to check if a text is English

def is_english(text: str) -> bool:
    try:
        lang = detect(text)
        return lang == 'en'
    except LangDetectException:
        # Could not detect language (e.g., empty or invalid text)
        return False

# 3. Iterate through documents and find non-English titles

non_english_docs = []

for doc in tqdm(collection.find({}, {'title': 1}), desc="Checking titles"):
    title = doc.get('title', '')
    if not title or not is_english(title):
        non_english_docs.append(doc)

# 4. Output results

print(f"Found {len(non_english_docs)} non-English titles:")
for doc in non_english_docs:
    print(doc['_id'], doc.get('title', ''))

# Optional: Update documents to flag them
# collection.update_many(
#     {'_id': {'$in': [d['_id'] for d in non_english_docs]}},
#     {'$set': {'non_english_title': True}}
# )
