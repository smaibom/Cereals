from flask import Blueprint, render_template
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html', name = "")
    return render_template('index.html', name = current_user.name)
