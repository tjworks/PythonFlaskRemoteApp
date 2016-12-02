from pymongo import MongoClient
from bson.json_util import dumps
from flask import Flask,render_template,jsonify,json,request

client = MongoClient('mongodb:27017')

db=client.test

user={"name": "Jennifer", "location":"Taipei"}
user["lastname"] = "Lee"

#print db["users"].insert(user)
obj=db["users"].find_one({"name":"Jennifer"})
print dumps(obj)
