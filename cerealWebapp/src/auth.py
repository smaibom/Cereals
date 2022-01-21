from flask import Blueprint, render_template, redirect,url_for, request,flash, current_app
from .authdbfunctions import check_user, gen_user, get_user
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_httpauth import HTTPBasicAuth

"""
Blueprint for functions related to login and creating users. This file holds the 
"""

auth = Blueprint('auth', __name__)

auth_api = HTTPBasicAuth()
@auth_api.verify_password
def verify_password(username, password):
    """
    Using httpbasicauth as the normal login system does not work for the api request part. Checks if the user exist in database and the password is correct.
    """
    return check_user(username,password)


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
    login_status = check_user(name,pwd)
    if not login_status:
        current_app.logger.info('%s failed to login' % name)
        flash('Invalid login credentials')
        return redirect(url_for('auth.login')) 
    current_app.logger.info('%s failed to authenticated on api' % login_status)
    user = get_user(name)
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
    user = get_user(name)
    if user: 
        flash('Name already in use')
        return redirect(url_for('auth.signup'))

    #New user created, added to DB and redirect to login
    pwd = generate_password_hash(pwd, method='sha256')
    gen_user(name,pwd)
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    name = current_user.name
    logout_user()
    current_app.logger.info('%s logged out' % name)
    return redirect(url_for('main.index'))

