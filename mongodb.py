import pymongo
import bson.json_util as json_util
import json
import datetime
from datetime import time
from cerberus import Validator


def get_users_collection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["mipt"]
    mycol = mydb["users"]
    mycol.create_index("user_id", unique=True)
    return mycol


def add_user(data: dict):

    user_schema = {
        'userid': {
            'type': 'string',
                    'required': True
        },
        'username': {
            'type': 'string',
            'required': True
        },
        'gender': {
            'type': 'string',
            'required': True
        },
        'age': {
            'type': 'string',
            'required': True
        },
        'city': {
            'type': 'string',
            'required': True
        },
        'bio': {
            'type': 'string',
            'required': True
        },
        'active': {
            'type': 'string',
            'required': True
        },
    }

    user_validator = Validator(user_schema)

    if user_validator.validate(data):
        try:
            user = {
                "user_id": data['userid'],
                "username": data["username"],
                "gender": data["gender"],
                "created": str(datetime.datetime.now()),
                "age": data["age"],
                "city": data["city"],
                "bio": data["bio"],
                "active": data["active"]
            }
            mycol = get_users_collection()
            mycol.insert_one(user)
            return f"Successfully added user: {user['username']}"
        except Exception as error:
            return f"Error {str(error)}"
    else:
        return user_validator.errors


def list_users():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["mipt"]
    mycol = mydb["users"]
    users_list = list(mycol.find({}, {"_id": 0}))
    return users_list
