from functools import wraps


def is_owner_or_admin(f):
    @wraps
    def decorated_function(*args, **kwargs):

        return f(*args, **kwargs)

    return decorated_function

