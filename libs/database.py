#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pymongo import MongoClient, errors
from bson import ObjectId

def conn_mongodb(uri, database):
    return MongoClient(uri)[database]        

def find(mongo_collection, fltr):
    if fltr is None:
        return mongo_collection.find()
    else:
        return mongo_collection.find(fltr)

def findById(mongo_collection, document_id):
    return mongo_collection.find_one({'_id': ObjectId(document_id)})

def insert(mongo_collection, data, bulk):
    if bulk:
        return mongo_collection.insert_many(data).inserted_id
    else:
        return mongo_collection.insert_one(data).inserted_id

def update(mongo_collection, fltr, data):
    return mongo_collection.update_one(fltr, {'$set': data}, upsert=False)

def updateById(mongo_collection, document_id, data):
    return mongo_collection.update_one({'_id': ObjectId(document_id)}, data)

def delete(mongo_collection, document_id, bulk):
    if bulk:
        return mongo_collection.delete_many(document_id)
    else:
        return mongo_collection.delete_one({'_id': ObjectId(document_id)})

def ifExist(mongo_collection, document_id):
    if mongo_collection.find({'_id': ObjectId(document_id)}).count() > 0:
        return True
    else:
        return False

def count(mongo_collection, fltr):
    """Find data return values"""
    if fltr is None:
        return mongo_collection.count_documents({})
    else:
        return mongo_collection.count_documents(fltr)

def collection_iterator(cursor, limit=1000):
        skip = 0
        while True:
            results = find(cursor, None).skip(skip).limit(limit)
            try:
                results.next()
            except StopIteration:
                break
            for result in results:
                yield result
            skip += limit