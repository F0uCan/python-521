
import functools
import flask

def login_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if not flask.session.get('authenticated'):
            return flask.redirect('/sign-in')
        else:
            return function(*args, **kwargs)
    return wrapper