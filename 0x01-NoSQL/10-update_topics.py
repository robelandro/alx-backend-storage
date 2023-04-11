#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """


def update_topics(mongo_collection, name, topics):
    """
    The function changes all topics of a school document based on the name.
    """
    query = {"name": name}
    n_values = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, n_values)
