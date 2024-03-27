#!/usr/bin/env python3
"""
Creates a redis client instance class
"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """
    Redis class to store redis instance and flush the instance
    """

    def __init__(self):
        """
        Constructor method
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a random key(uuid) and stores it
        """
        redis_key = str(uuid4())
        self._redis.set(redis_key, data)

        return redis_key
