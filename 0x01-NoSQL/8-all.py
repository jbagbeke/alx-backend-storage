#!/usr/bin/env python3
"""
MongoDB - Lists all documents in a collection
"""
import pymongo

def list_all(mongo_collection):
    """
    Lists all docs in a mongodb collection
    """
    
    if not mongo_collection:
        return []

    return [doc for doc in mongo_collection.find()]