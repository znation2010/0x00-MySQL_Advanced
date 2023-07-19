#!/usr/bin/env python3
'''A module for using the Redis NoSQL data storage.
'''
from functools import wraps
import redis
import sys
from typing import Union, Optional, Callable
from uuid import uuid4


def replay(method: Callable):
    """
    Decorator to print the replay of method calls.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])
    count = method.__self__.get(key)
    i_list = method.__self__._redis.lrange(i, 0, -1)
    o_list = method.__self__._redis.lrange(o, 0, -1)
    queue = list(zip(i_list, o_list))
    print(f"{key} was called {decode_utf8(count)} times:")
    for k, v in queue:
        k = decode_utf8(k)
        v = decode_utf8(v)
        print(f"{key}(*{k}) -> {v}")


def call_history(method: Callable) -> Callable:
    """
    Decorator to keep the call history of the method.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res
    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def decode_utf8(b: bytes) -> str:
    """
    Decodes bytes to utf-8 encoded string.
    """
    return b.decode('utf-8') if type(b) == bytes else b


class Cache:
    """
    Cache class that interacts with Redis to store and retrieve data.
    """

    def __init__(self):
        """
        Initializes the Cache and connects to the Redis server.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the data in Redis with a random key and returns the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """
        Retrieves the data associated with the given key from Redis.
        """
        res = self._redis.get(key)
        return fn(res) if fn else res

    def get_str(self, data: bytes) -> str:
        """
        Converts bytes to a UTF-8 encoded string.
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        Converts bytes to an integer using sys.byteorder.
        """
        return int.from_bytes(data, sys.byteorder)
