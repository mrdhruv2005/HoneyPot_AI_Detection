from pymongo import MongoClient
import os

uri = "mongodb://localhost:27017"
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    client.server_info()
    print("SUCCESS: Connected to MongoDB")
except Exception as e:
    print(f"FAILURE: Could not connect to MongoDB: {e}")
