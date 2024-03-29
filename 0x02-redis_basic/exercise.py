#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a method is called.
    :param method: The `method` parameter is a function
    :type method: Callable
    :return: The function `count_calls` returns a function
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    :param method: The `method` parameter is a function
    :type method: Callable
    :return: The function `count_calls` returns a function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    :param method: The `method` parameter is a function
    :type method: Callable
    :return: None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print(f"{name} was called {calls} times:")
    inputs = cache.lrange(f"{name}:inputs", 0, -1)
    outputs = cache.lrange(f"{name}:outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


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

    @call_history
    @count_calls
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
