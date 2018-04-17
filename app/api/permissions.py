from app import cas, DEV
from app.data.user import User
from functools import wraps
from flask import abort


def valid_call(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if DEV or cas.token:
            return f(*args, **kwargs)
        abort(403)
    return wrapped_function

def is_admin(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if DEV: # If we are in a dev environment
            return f(*args, **kwargs)

        u = User.query.filter_by(username=cas.username).one()
        if u.is_admin:
            return f(*args, **kwargs)
        abort(403)
    return wrapped_function