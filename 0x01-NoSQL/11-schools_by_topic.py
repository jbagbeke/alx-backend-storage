#!/usr/bin/env python3
"""
MongoDB - Returns the list of school having a specific topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    
    if not mongo_collection or not topic:
        return []
    
    return [sch for sch in mongo_collection.find({"topics": str(topic)})]