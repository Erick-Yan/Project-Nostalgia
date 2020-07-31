import os
import requests
import urllib.parse
import datetime as dt

from flask import redirect, render_template, request, session
from functools import wraps

ALLOWED_EXTENSIONS = {'mp3', 'png', 'jpg', 'jpeg'}

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def date_conversion(d):
    year, month, day = d.split('-')
    date = dt.datetime(int(year), int(month), int(day))
    return date

from uuid import uuid4
def make_unique(string):
    ident = uuid4().__str__()[:8]
    return f"{ident}-{string}"