#!/usr/bin/env python3
"""
Web Redis basic
"""
from functools import wraps
import redis
import requests
from typing import Callable
import requests


redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator for counting
    :param method: The `method` parameter is a function
    :type method: Callable
    :return: The function `count_requests` returns a function"""
    @wraps(method)
    def wrapper(url):
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
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
