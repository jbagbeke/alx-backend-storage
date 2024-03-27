#!/usr/bin/env python3
"""
MongoDB - Lists all documents in a collection
"""
import pymongo

if __name__ == '__main__':
    def list_all(mongo_collection):
        """
        Lists all docs in a mongodb collection
        """
        mongo_collection.find()
    
    