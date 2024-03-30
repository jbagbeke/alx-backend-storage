#!/usr/bin/env python3
"""
Obtain the HTML content of a particular URL and returns it.
"""
import requests
import redis
from typing import Callable
from functools import wraps


def redisCount(method: Callable) -> Callable:
    """
    Returns a wrapper that counts number of times
    a url was called
    """
    redisCache = redis.Redis()

    @wraps(method)
    def urlCount(*args):
        urlKey = "count:{}".format(args[0])
        urlResult = redisCache.get(urlKey)

        if urlResult:
            redisCache.incr(urlKey)
        else:
            redisCache.set(urlKey, 1)

        url_request_result = method(*args)
        print(url_request_result)
        redisCache.setex(args[0], 10, url_request_result)

        return url_request_result
    return urlCount

   
@redisCount
def get_page(url: str) -> str:
    """
    Implements caching system with url"""
    
    try:
        urlRequest = requests.get(url)    
    except Exception:
        print("Invalid URL passed")

    return urlRequest.text
