#!/usr/bin/env python3
"""
MongoDB - Changes all topics of a school document based on the name
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name
    """
    
    if not mongo_collection or not name or not topics:
        return
    
    mongo_collection.update_many({"name": str(name)}, {"$set": {"topics": topics}})