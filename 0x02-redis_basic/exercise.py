#!/usr/bin/env python3
"""
Creates a redis client instance class
"""
import redis
from typing import Union, Callable, Any
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

    @property
    def get(self, key: str, fn: Callable=None) -> Any:
        """
        Converts data to back to desired format
        """

        redis_response = self._redis.get(key)

        if redis_response:
            if fn and fn == int:
                return self.get_int(redis_response)
            elif fn and fn == str:
                return self.get_str(redis_response)

            return redis_response.decode('utf-8')

    def get_str(self, redis_response: str) -> str:
        """
        Decodes redis response with utf-8
        """
        return redis_response.decode('utf-8')

    def get_int(self, redis_response: str) -> int:
        """
        Decodes redis response with utf-8 and type casts to int
        """

        return int(redis_response.decode('utf-8'))
