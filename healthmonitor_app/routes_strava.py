from flask import Blueprint, redirect, flash, url_for, request, session
from flask.templating import render_template
from flask_login import login_required, current_user

import logging, inspect

from .backend import get_strava_activities
from .models import User
from .stravaapi import StravaUser
from . import db

# Create a blueprint named 'strava'. Follow along tutorial at:
# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
strava_blueprint = Blueprint('strava_blueprint', __name__,
                             url_prefix='/strava')

SERVER_URL = "http://127.0.0.1:5000"

@strava_blueprint.route('/authorize/url')
@login_required
def authorize_url():
    """Reroutes to strava authorization url -> codehandler"""
    # Create instance of StravaUser object
    strava_user = StravaUser()
    # Redirect user to authorization url
    return redirect(strava_user.generate_authorize_url(
        redirect_to=SERVER_URL + url_for(
                        'strava_blueprint.strava_codehandler')))

@strava_blueprint.route('/authorize/codehandler', methods=['GET'])
@login_required
def strava_codehandler():
    """Reroutes to dashboard"""

    try:
        code = request.args['code']
    except:
        flash('Authorization invalid. Please try again.', 'warning')
        return redirect(url_for('main_blueprint.dashboard'))

    # Create instance of StravaUser object
    strava_user = StravaUser()
    strava_user.authorize_user(code)

    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()
    # Set tokens for user
    user.strava_access_token = strava_user.access_token
    user.strava_refresh_token = strava_user.refresh_token
    user.strava_expires_at = strava_user.expires_at
    # Commit changes
    db.session.commit()

    flash('Strava has been authorized successfully!')
    return redirect(url_for('user_blueprint.dashboard'))

@strava_blueprint.route('/deauthorize')
@login_required
def deauthorize_url():
    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()

    # Create instance of StravaUser object
    strava_user = StravaUser(access_token=user.strava_access_token,
                            refresh_token=user.strava_refresh_token,
                            expires_at=user.strava_expires_at)
    
    # Delete tokens from user in database
    user.strava_access_token = None
    user.strava_refresh_token = None
    user.strava_expires_at = None
    db.session.commit()

    # Deauthorize
    strava_user.deauthorize_user()

    flash('Strava has been deauthorize successfully!')
    return redirect(url_for('user_blueprint.dashboard'))


@strava_blueprint.route('/profile')
@login_required
def strava_profile():
    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()

    # Create instance of StravaUser object
    strava_user = StravaUser(access_token=user.strava_access_token,
                            refresh_token=user.strava_refresh_token,
                            expires_at=user.strava_expires_at)
    
    # Compare access token and update if necessary
    if user.strava_access_token != strava_user.access_token:
        user.strava_access_token = strava_user.access_token
        user.strava_refresh_token = strava_user.refresh_token
        user.strava_expires_at = strava_user.expires_at
        db.session.commit()
    
    # Get strava profile
    strava_user.get_strava_profile()

    return render_template('strava_profile.html',
                            firstname=strava_user.firstname,
                            lastname=strava_user.lastname,
                            weight=strava_user.weight)

@strava_blueprint.route('/refresh_activities')
@login_required
def refresh_activities():
    # Hasn't been refreshed -> get from API
    refresh_time = get_strava_activities()

    # Set in session
    session['refresh_time'] = refresh_time

    return redirect(url_for('user_blueprint.show_activities'))