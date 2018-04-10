from app import cas
from app.data.user import User
from functools import wraps
from flask import abort


def valid_call(f):
    @wraps
    def wrapped_function(*args, **kwargs):
        if cas.token:
            return f(*args, **kwargs)
        abort(403)
    return wrapped_function

@valid_call
def is_admin(f):
    @wraps
    def wrapped_function(*args, **kwargs):
        u = User.query.filter_by(username=cas.username).one()
        if u.is_admin:
            return f(*args, **kwargs)
        abort(403)
    return wrapped_function