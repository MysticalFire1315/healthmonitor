from datetime import datetime, timedelta
from flask import redirect, current_app
from flask_login import current_user
from flask_login.utils import login_url as make_login_url
from functools import wraps
from time import localtime, time

from . import db
from .ml import Clustering
from .models import User, Activity
from .stravaapi import StravaUser
from .utility import month_to_words

def get_strava_activities():
    """
    Get activities from Strava's API. Stores activity data in database.

    :return: A tuple containing the timestamp when the activities were taken.
    :rtype: int
    """
    
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
    
    # Get strava activities
    strava_user.get_strava_activities()

    # Delete all Activity models
    db.session.query(Activity).delete()

    # Loop through activities to add to database
    for activity in strava_user.activity_list:
        # Initialise Activity model
        new_activity = Activity(
            name = activity['name'],
            type = activity['type'],
            distance = activity['distance'],
            moving_time = activity['moving time'],
            elapsed_time = activity['elapsed time'],
            start_date_local = datetime.fromtimestamp(
                                            activity['start date local']),
            manual_entry = activity['manual entry'],
            average_speed = activity['average speed']
        )

        # Add to database
        db.session.add(new_activity)
        db.session.commit()

    # Get activity list
    return time()

def weekly_hours():
    """
    Calculate the number of hours of moving time for the last week.
    More info at: https://bit.ly/3l61Oc3

    :return: The number of hours of moving time in the last week.
    :rtype: float
    """

    # Get current timestamp
    current_time = datetime.now()
    # Set earliest time (1 week before -> 7 days)
    earliest_time = current_time - timedelta(days=7)

    # Get activities between that time
    activities = Activity.query.filter(
            Activity.start_date_local <= current_time
        ).filter(
            Activity.start_date_local >= earliest_time
        )
    
    total_moving_time = 0

    # Loop through to calculate total moving time
    for activity in activities:
        total_moving_time += activity.moving_time
    
    return round(total_moving_time/3600, 2)

def find_usual_activity_time():
    """
    Identify the usual times when activities occur.
    """

    # Get activities from database
    activities = Activity.query

    # Make a list of start timestamps
    start_timestamps = []
    for activity in activities:
        start_timestamps.append(activity.start_date_local)
    
    # Initialise Clustering object
    cluster = Clustering()

    # Get period where cluster was formed and cluster items
    period, items = cluster.cluster_timestamps(start_timestamps)

    if period > 0:
        groups = []
        for group in items:
            subgroup = []
            for timestamp in group:
                subgroup.append(Activity.query.filter_by(
                                       start_date_local=timestamp).first())
            groups.append(subgroup)
        return period, groups
    return period, 

def not_login_required(func):
    """
    Similar to :func:`flask_login.login_required`, except that if a view
    is decorated with this, it will ensure the current user is not logged in
    or authenticated before calling the actual view. (If they are, it
    redirects the user to the :attr:`LoginManager.not_login_view` if set,
    otherwise to endpoint '/'.) For example::

        @app.route('/login')
        @not_login_required
        @def login():
            pass
    
    This is useful for views such as login and signup where the user cannot
    already be authenticated.

    :param func: The view function to decorate.
    :type func: function
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated:
            try:
                return redirect(make_login_url(
                    current_app.login_manager.not_login_view))
            except:
                return redirect(make_login_url('/'))
        return func(*args, **kwargs)
    return decorated_view

def display_time(seconds_since_epoch):
    """
    Convert a Seconds since Epoch representation of time to a human readable
    string for display. Format of the return string will be as follows:
        hour(`int`):min(`int`):sec(`int`) on day(`int`) mon(`str`) year(`int`)

    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: A human-readable representation of the input time.
    :rtype: str
    """

    # First convert to struct_time object
    struct_time_obj = localtime(seconds_since_epoch)

    if struct_time_obj.tm_hour > 11:
        if struct_time_obj.tm_hour == 12:
            hour = 12
        else:
            hour = struct_time_obj.tm_hour - 12
        time_of_day = 'PM'
    else:
        if struct_time_obj.tm_hour == 0:
            hour = 12
        else:
            hour = struct_time_obj.tm_hour
        time_of_day = 'AM'

    # Initialise return string
    return_str = ' '.join([str(hour) + ':' +
                f'{struct_time_obj.tm_min:02}' + ':' +
                f'{struct_time_obj.tm_sec:02}', time_of_day, 'on',
                str(struct_time_obj.tm_mday),
                month_to_words(struct_time_obj.tm_mon),
                str(struct_time_obj.tm_year)])
    
    return return_str

