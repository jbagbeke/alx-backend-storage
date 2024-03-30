#!/usr/bin/env python3
"""
Obtain the HTML content of a particular URL and returns it.
"""
import requests
import redis
from typing import Callable
from functools import wraps


redisCache = redis.Redis()


def redisCount(method: Callable) -> Callable:
    """
    Returns a wrapper that counts number of times
    a url was called
    """
    @wraps(method)
    def urlCount(*args):
        urlCount = "count:" + args[0]
        urlCache = "cache:" + args[0]

        urlResult = redisCache.get(urlCache)
        redisCache.incr(urlCount)

        if not urlResult:
            url_html = method(*args)
            redisCache.setex(urlCache, 10, url_html)

            return url_html
        return urlResult.decode('utf-8')

    return urlCount


@redisCount
def get_page(url: str) -> str:
    """
    Implements caching system with url"""

    urlRequest = requests.get(url)

    return urlRequest.text
