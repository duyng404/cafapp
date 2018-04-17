from app import cas, DEV
from app.data.user import User
from functools import wraps
from flask import abort
from flask_cas import login_required

def valid_call(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if DEV or cas.token:
            return f(*args, **kwargs)
        abort(403)
    return wrapped_function

@valid_call
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

def our_login_required(f):
    @wraps(f)
    def inner_function(*args, **kwargs):
        if DEV:
            return f(*args, **kwargs)
        return login_required(f)(*args, **kwargs)
    return inner_function

