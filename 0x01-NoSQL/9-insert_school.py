#!/usr/bin/env python3
"""
MongoDB - Inserts a new document in a collection based on kwargs
"""
import pymongo

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    """
    
    if not mongo_collection or not kwargs:
        return []
    
    mongo_doc = {key: val for key, val in kwargs.items()}

    insert_doc_val = mongo_collection.insert_one(mongo_doc)
    return insert_doc_val.inserted_id