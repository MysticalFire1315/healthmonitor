from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user


main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def index():
    # If user is logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('user_blueprint.dashboard'))
    
    # Otherwise show index page
    return render_template('index.html')

@main_blueprint.route('/about')
def about():
    return render_template('about.html')

@main_blueprint.route('/help')
def help():
    return render_template('help.html')
