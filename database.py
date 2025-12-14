# database.py
from pymongo import MongoClient
# from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
# client = AsyncIOMotorClient(MONGO_URL)

db = client["TODO"]
collection = db["student"]
users_collection = db["users"]

def create(data):
    data = dict(data)
    response = collection.insert_one(data)
    return str(response.inserted_id)


def getAll():
    response = collection.find({})
    # response = collection.find({}, {"_id" : 0, "name": 0})
    data = []
    for i in response:
        i["_id"] = str(i["_id"])    
        # i["_id"] = str(i["_id"])
        data.append(i)
        print("Fetched data:", data)
    return data



