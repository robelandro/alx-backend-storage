#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def insert_school(mongo_collection, **kwargs):
    """
    The function inserts a new document in a collection based on kwargs.
    """
    return mongo_collection.insert(kwargs)
