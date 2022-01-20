from flask import Blueprint, render_template, redirect,url_for, request,flash, current_app
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

"""
Blueprint for functions related to login and creating users. This file holds the 
"""

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """
    Function that redirects to login page
    """
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Post function of the login page, used when user types in login info
    """
    #Get login info
    name = request.form.get('name')
    pwd = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # Check for user, if wrong we send them back with a message that it is wrong
    user = User.query.filter_by(name=name).first()
    if not user or not check_password_hash(user.pwd, pwd):
        flash('Please check your login details and try again.')
        current_app.logger.info('%s failed to login' % name)
        return redirect(url_for('auth.login')) 

    #Login user, return to main index
    login_user(user, remember=remember)
    current_app.logger.info('%s Logged in successfully' % name)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    #Get info user wrote in on signup page
    name = request.form.get('name')
    pwd = request.form.get('password')

    #Check if user exist already, if so redirect user back to signup page to try again
    user = User.query.filter_by(name=name).first()
    if user: 
        flash('Name already in use')
        return redirect(url_for('auth.signup'))

    #New user created, added to DB and redirect to login
    new_user = User(name=name, pwd=generate_password_hash(pwd, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    current_app.logger.info('%s added as a user to DB' % name)
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    name = current_user.name
    logout_user()
    current_app.logger.info('%s logged out' % name)
    return redirect(url_for('main.index'))

