from functools import wraps


class CachedItem:
    def __init__(self, key: tuple, data: str, counter: int):
        self.key = key
        self.data = data
        self.counter = counter

    def __eq__(self, other):
        return self.key == other


def response_from_db(obj: CachedItem):
    obj.counter += 1
    return f'[from cache] {obj.data}'


def cache(limit=10):
    def shaper(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            keys = (args, tuple(kwargs.items()))
            for obj in CachedData:
                if keys == obj:
                    return response_from_db(obj)
            data = function(keys)
            if len(CachedData) >= limit:
                CachedData.sort(key=lambda i: i.counter, reverse=True)
                CachedData.pop()
            CachedData.append(CachedItem(keys, data, 1))
            return data
        return wrapper
    CachedData = []  # [CachedItem(key,data,counter), CachedItem(key,data,counter)]
    return shaper

