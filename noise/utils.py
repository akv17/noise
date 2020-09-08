def timer(func):
    from time import time
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time()
        rv = func(*args, **kwargs)
        rt = round(time() - st, 5)
        print(func.__name__, rt)
        return rv

    return wrapper
