import redis
import json
from pymongo import MongoClient

# Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
print("=== REDIS SESSIONS ===")
for key in r.keys("session:*"):
    data = json.loads(r.get(key))
    print(f"\n{key}:")
    print(f"  Messages: {len(data.get('history', []))}")
    print(f"  Intelligence: {data.get('intelligence', {})}")
    print(f"  Last Updated: {data.get('updated_at', 'N/A')}")

print("\n\n=== REDIS STATS ===")
for key in r.keys("stats:public_guest:*"):
    if not "activity" in key:  # Skip hourly activity for brevity
        value = r.get(key)
        print(f"{key}: {value}")

# MongoDB
try:
    client = MongoClient("mongodb+srv://jpjangid710_db_user:Demo%40123@mycluster.krhtdot.mongodb.net/erp_db")
    db = client.erp_db
    print("\n\n=== MONGODB COLLECTIONS ===")
    for collection_name in db.list_collection_names():
        count = db[collection_name].count_documents({})
        print(f"{collection_name}: {count} documents")
        
        # Show sample document if exists
        if count > 0:
            sample = db[collection_name].find_one()
            print(f"  Sample fields: {list(sample.keys())}")
except Exception as e:
    print(f"\nMongoDB Error: {e}")
