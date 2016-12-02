from pymongo import MongoClient
client = MongoClient('mongodb:27017')

db=client.test

user={"name": "Jennifer", "location":"Taipei"}
user["lastname"] = "Lee"

print db["users"].insert(user)
