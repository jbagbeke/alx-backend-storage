#!/usr/bin/env python3
"""
Creates a redis client instance class
"""
import redis
from functools import wraps
from typing import Union, Callable, Any, Optional
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """
    Wrapper function to keep track of number of times
    a method was called
    """
    @wraps(method)
    def cache_method_wrapper(self, *args, **kwargs):
        method_calls = self._redis.get(str(method.__qualname__))

        if method_calls:
            self._redis.incr(str(method.__qualname__))
        else:
            self._redis.set(str(method.__qualname__), 1)

        redis_key = method(self, *args, **kwargs)
        return redis_key
    return cache_method_wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores method params and outputs when the method is called
    """
    
    @wraps(method)
    def method_call_history(self, *args, **kwargs):
        inputs_key = str(method.__qualname__) + ":inputs"
        outputs_key = str(method.__qualname__) + ":outputs"
        
        self._redis.rpush(inputs_key, str(args))
        redis_key_output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, redis_key_output)
        
        return redis_key_output
    return method_call_history


def replay(replay_func: Callable) -> None:
    """
    Displays the history of calls of a particular function
    """

    func_name = replay_func.__qualname__
    func_instance = replay_func.__self__
    inputs_key = func_name + ":inputs"
    outputs_key = func_name + ":outputs"

    func_count = func_instance._redis.get(func_name)
    func_inputs = func_instance._redis.lrange(inputs_key, 0, -1)
    func_outputs = func_instance._redis.lrange(outputs_key, 0, -1)

    zipped_input_output = zip(func_inputs, func_outputs)

    print("{} was called {} times".format(func_name, func_count.decode('utf-8')))

    for io in zipped_input_output:
        input, output = io
        print("{}({}) -> {}".format(func_name, input, output.decode('utf-8')))


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

    @call_history
    @count_calls
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
