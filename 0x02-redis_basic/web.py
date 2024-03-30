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
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper for decorator """
        redisCache.incr(f"count:{url}")
        cached_html = redisCache.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redisCache.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@redisCount
def get_page(url: str) -> str:
    """
    Implements caching system with url"""

    urlRequest = requests.get(url)

    return urlRequest.text
