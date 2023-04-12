#!/usr/bin/env python3
"""
Redis basic
"""
import redis
import uuid
from typing import Union


class Cache:
    _redis = redis.Redis()

    def __init__(self) -> None:
        """
        This is a constructor method that clears all data.
        """
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
