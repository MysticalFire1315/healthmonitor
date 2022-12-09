from flask import (Blueprint, flash, redirect, render_template, session,
                   url_for)
from flask_login import login_required, current_user
from time import time

from .backend import (display_time, find_usual_activity_time, 
                      get_strava_activities, weekly_hours)
from .models import User, Activity

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/user')

@user_blueprint.route('/dashboard')
@login_required
def dashboard():
    """Does not redirect away. Most views should redirect here."""
    
    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()

    # Check if user has authenticated strava
    if user.strava_access_token is None:
        return render_template('dashboard.html', authorized=False)
    
    # Get strava activities
    if 'refresh_time' in session:
        # Refresh time in session means activities is also in session
        if (session['refresh_time'] + 3600) < time():
            # Check if the last refresh time + 1hr is less than
            # current time (ie. refresh time was more than 1hr ago)
            # TRUE -> Get activities from API
            refresh_time = get_strava_activities()

            # Set in session
            session['refresh_time'] = refresh_time
        else:
            # Otherwise get from session
            refresh_time = session['refresh_time']
    else:
        # Hasn't been refreshed -> get from API
        refresh_time = get_strava_activities()

        # Set in session
        session['refresh_time'] = refresh_time

    recommended_hours = user.recommended_hours


    # Try to find any patterns in start timestamps
    period, cluster_groups = find_usual_activity_time()
    
    # Clusters will only be found if period > 0
    if period < 0:
        return render_template('dashboard.html', authorized=True,
                                weekly_hours=weekly_hours(),
                                recommended_hours=recommended_hours)
    
    filtered_weekdays = []
    for subgroup in cluster_groups:
        # Calculate average start time for each subgroup
        avg_start_time = 0
        for item in subgroup:
            day_in_period = item.start_date_local.timetuple().tm_yday % period
            avg_start_time += item.start_date_local.hour
            avg_start_time += item.start_date_local.minute/60

        # Average start time for the group
        avg_start_time = avg_start_time/len(subgroup)
        filtered_weekdays.append([day_in_period, avg_start_time])

    # Get total moving time in last week
    return render_template('dashboard.html', authorized=True,
                            weekly_hours=weekly_hours(),
                            recommended_hours=recommended_hours,
                            period=period, weekdays=filtered_weekdays)
    
    

@user_blueprint.route('/activities')
@login_required
def show_activities():

    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()

    # Check if user has authenticated strava
    if user.strava_access_token:
        # Get strava activities
        if 'refresh_time' in session:
            # Refresh time in session means activities is also in session
            if (session['refresh_time'] + 3600) < time():
                # Check if the last refresh time + 1hr is less than
                # current time (ie. refresh time was more than 1hr ago)
                # TRUE -> Get activities from API
                refresh_time = get_strava_activities()

                # Set in session
                session['refresh_time'] = refresh_time
            else:
                # Otherwise get from session
                refresh_time = session['refresh_time']
        else:
            # Hasn't been refreshed -> get from API
            refresh_time = get_strava_activities()

            # Set in session
            session['refresh_time'] = refresh_time
    else:
        flash('Authorize Strava to access this page. More information available at Help', 'warning')
        return redirect(url_for('user_blueprint.dashboard'))
    
    # Get all activities
    activities = Activity.query
    
    return render_template('show_activities.html',
                            refresh_time=display_time(refresh_time),
                            activities=activities)


@user_blueprint.route('/settings')
@login_required
def settings():
    # Get user from database
    user = User.query.filter_by(email=current_user.email).first()

    table_data = {
        'Username': user.name,
        'Email': user.email,
        'Strava Authorized': False, 
        'Recommended Hours': round(user.recommended_hours/3600, 2)
    }

    # Check if strava has been authorized (ie. access token exists)
    if user.strava_access_token:
        table_data['Strava Authorized'] = True
    

    return render_template('settings.html',
                            table_data=table_data)