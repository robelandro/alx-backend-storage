#!/usr/bin/env python3
"""
Web Redis basic
"""
from functools import wraps
import redis
import requests
from typing import Callable
import requests


_redis = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator for counting
    :param method: The `method` parameter is a function
    :type method: Callable
    :return: The function `count_requests` returns a function"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """
        wrapper function
        """
        _redis.incr(f"count:{args[0]}")

        html = _redis.get("html-cache:{args[0]}")
        if html is not None:
            return html.decode("utf-8")
        html = method(*args, **kwargs)
        _redis.setex(f"html-cache:{args[0]}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a  URL
    :param url: The `url` parameter is a string
    :type url: str
    :return: The function `get_page` returns a string"""
    req = requests.get(url)
    return req.text
