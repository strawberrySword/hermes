from pymongo import DeleteOne, MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["hermes"]
collection = db["articles"]

pipeline = [
    {
        "$group": {
            "_id": "$title",                      # Field to deduplicate
            "ids": {"$push": "$_id"},
            "count": {"$sum": 1}
        }
    },
    {
        "$match": {
            "count": {"$gt": 1}
        }
    }
]

duplicates = list(collection.aggregate(pipeline))
print(duplicates)
# Prepare bulk delete operations
bulk_ops = []
for group in duplicates:
    # Keep one ID, delete the rest
    ids_to_delete = group["ids"][1:]  # skip first
    for _id in ids_to_delete:
        bulk_ops.append(DeleteOne({"_id": _id}))

# Execute bulk delete
if bulk_ops:
    result = collection.bulk_write(bulk_ops)
    print(f"Deleted {result.deleted_count} duplicate documents.")
else:
    print("No duplicates found.")
