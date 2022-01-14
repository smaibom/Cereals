from flask import Blueprint, render_template, redirect,url_for, request,flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user

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
        return redirect(url_for('auth.login')) 

    #Login user, return to main index
    login_user(user, remember=remember)
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
        return redirect(url_for('auth.signup'))

    #New user created, added to DB and redirect to login
    new_user = User(name=name, pwd=generate_password_hash(pwd, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

