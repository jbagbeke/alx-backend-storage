#!/usr/bin/env python3
"""
Creates a redis client instance class
"""
import redis
from typing import Union, Callable, Any, Optional
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

    def get(self, key: str, fn: Optional[Callable]=None) -> Any:
        """
        Converts data to back to desired format
        """

        redis_response = self._redis.get(key)

        if redis_response:
            if fn:
                return fn(redis_response)
            return redis_response        
        return None

    def get_str(self, key: str) -> str:
        """
        Calls get function ecodes redis response with utf-8
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Calls get function with int function which type casts to int
        """
        return self.get(key, lambda x: int(x))
