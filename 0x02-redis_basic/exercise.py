#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    This class is a wrapper around the Redis client.
    """

    def __init__(self) -> None:
        """
        This is a constructor method that clears all data.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This Python function stores data in Redis using a random key.

        :param data: The `data` to be stored in Redis.
        :type data: Union[str, bytes, int, float].
        :return: a string which is the unique identifier (id).
        """
        id = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        This is a Python function that retrieves a value from Redis.
        
        :param key: A string representing the key.
        :type key: str
        :param fn: The parameter `fn` an optional argument of type `Callable`
        :type fn: Optional[Callable]
        :return: The function `get` returns
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        This function retrieves a string value
        
        :param key: The `key` parameter is a string
        :type key: str
        :return: The function `get_str` is returning a string value
        """
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        This function retrieves an integer value
        
        :param key: The `key` parameter is a string
        :type key: str
        :return: This function returns an integer value
        """
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
