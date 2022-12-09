from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import db
from .backend import not_login_required
from .forms import LoginForm, SignupForm
from .hashing import hash_item, verify_item
from .models import User


auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

@auth_blueprint.route('/login')
@not_login_required
def login():
    # If not, show form
    form = LoginForm()
    return render_template('login.html', form=form)

@auth_blueprint.route('/signup')
@not_login_required
def signup():
    # If not, show form
    form = SignupForm()
    return render_template('signup.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))

@auth_blueprint.route('/signup', methods=['POST'])
@not_login_required
def signup_post():
    # Used template from: https://do.co/3f1jIZK
    form = SignupForm()

    if form.validate_on_submit():
        # Code here will be run if form was submitted correctly

        # Get form data
        email = form.data['email']
        name = form.data['name']
        password = form.data['password']
        age_group = form.data['age_group']

        # If this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        # If a user is found, redirect back to signup page to try again
        if user:
            flash('Error: Email address already exists.', 'critical')
            return redirect(url_for('auth_blueprint.signup'))
        
        # Calculate recommended hours for age group
        if age_group == "0":
            # 3 days/week, 60 mins
            recommended_time = 3*60*60
        elif age_group == "1":
            # 5 hrs/week
            recommended_time = 5*60*60
        elif age_group == "2":
            # 7 days/week, 30 mins
            recommended_time = 7*30*60
        else:
            # same as if 2
            recommended_time = 7*30*60

        # Create a new user with the form data. Hash the password so the
        # plaintext version isn't saved.
        new_user = User(email=email, name=name,
                        password=hash_item(password),
                        recommended_hours=recommended_time)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Ensure that user is not logged in
        try:
            logout_user()
        except:
            login_user(user)
            logout_user()

        flash('User signed up successfully.', 'success')
        return redirect(url_for('auth_blueprint.login'))
    
    
    # This executes if form was not submitted correctly
    # First check password matches
    if form.errors['password']:
        flash('Error: Passwords must match', 'critical')
    elif form.errors['recaptcha']:
        flash('Error: Recaptcha must be completed', 'critical')
    else:
        flash('Error: Something went wrong. Please try again', 'critical')
    return redirect(url_for('auth_blueprint.signup'))

@auth_blueprint.route('/login', methods=['POST'])
@not_login_required
def login_post():
    # Used template from: https://do.co/3rFnOMf
    form = LoginForm()

    if form.validate_on_submit():
        # Code here will be run if form was submitted correctly

        # Get form data
        email = form.data['email']
        password = form.data['password']
        remember = form.data['remember']

        user = User.query.filter_by(email=email).first()

        # Check if the user actually exists
        # Take the user-suuplied password, has it, and compare it to the
        # hashed password in the database
        if not user:
            flash('Error: Email does not exist.', 'critical')
            return redirect(url_for('auth_blueprint.login'))
        elif not verify_item(user.password, password):
            flash('Error: Password is incorrect.', 'critical')
            return redirect(url_for('auth_blueprint.login'))
    
    # If the above check passes, then we know the user has the right
    # credentials
    login_user(user, remember=remember)
    flash('Login successful!', 'success')
    return redirect(url_for('user_blueprint.dashboard'))
