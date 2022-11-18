from os import environ as env
import time, datetime
from functools import wraps
from flask import session, redirect, url_for, flash, abort

app_config = {
    'APP_NAME': env.get('APP_NAME', 'Flask App'),
    'APP_ENV': env.get('APP_ENV', 'development'),
    'APP_VERSION': env.get('APP_VERSION', '0.0.1'),
    'APP_DESCRIPTION': env.get('APP_DESCRIPTION', 'Flask App'),
    'APP_AUTHOR': env.get('APP_AUTHOR', 'Flask App'),
    'APP_AUTHOR_EMAIL': env.get('APP_AUTHOR_EMAIL', 'Flask App'),
    'APP_CONTACT_NO': env.get('APP_CONTACT_NO', 'Flask App'),
    'APP_WEBSITE': env.get('APP_WEBSITE', 'Flask App'),
    'DB_HOST': env.get('DB_HOST', 'localhost'),
    'DB_PORT': env.get('DB_PORT', '3306'),
    'DB_USER': env.get('DB_USER', 'root'),
    'DB_PASSWORD': env.get('DB_PASSWORD', 'root'),
    'DB_NAME': env.get('DB_NAME', 'blog'),
    'Year': time.strftime("%Y"),
    'Month': time.strftime("%m"),
    'Day': time.strftime("%d"),
    'Date': datetime.datetime.now().strftime("%d-%m-%Y"),
    "GOOGLE_CLIENT_ID": env.get("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_ID"),
    "GOOGLE_CLIENT_SECRET": env.get("GOOGLE_CLIENT_SECRET", "GOOGLE_CLIENT_SECRET"),
    'TXT_API_KEY': env.get('TXT_API', 'TXT_API_KEY'),
    'TXT_URL': env.get('API_URL', 'API_URL'),
    'date_unix': time.mktime(datetime.date.today().timetuple()),
}


def load_config(app):
    app.secret_key = "ksbdvklhbslkdvhblhbf%^#&%*$Q(#&(*(HDFV"
    for key, value in app_config.items():
        app.config[key] = value


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'google_id' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "danger")
            return redirect(url_for('auth.login'))

    return wrap


def google_auth(function):  # a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()

    return wrapper
