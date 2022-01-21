from flask import current_app
from .models import User
from ... import db
from werkzeug.security import check_password_hash

def check_user(username,password):
    user = User.query.filter_by(name=username).first()
    if user and check_password_hash(user.pwd, password):
        return username
    current_app.logger.info('%s failed to authenticated on api' % username)

def get_user(username):
    user = User.query.filter_by(name=username).first()
    return user

def gen_user(username,password):
    new_user = User(name=username, pwd=password)
    db.session.add(new_user)
    db.session.commit()
    current_app.logger.info('%s added as a user to DB' % username)
