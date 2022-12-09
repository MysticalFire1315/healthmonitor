"""
Module for interacting with Strava's API using library *stravalib*
Reference: https://github.com/hozn/stravalib
"""

import time, calendar, flask, datetime, validators, logging, sys
import inspect # For debugging
from functools import wraps
from stravalib import Client, unithelper
import numpy as np

# Import other custom modules
from .utility import attrs, datetime_to_epochsecs, to_day_hr_arr
from .ml import Clustering


types = (
    "AlpineSki",
    "BackcountrySki",
    "Canoeing",
    "CrossCountrySkiing",
    "Crossfit",
    "EBikeRide",
    "Elliptical",
    "Golf",
    "Handcycle",
    "Hike",
    "IceSkate",
    "Kayaking",
    "NordicSki",
    "Ride",
    "RockClimbing",
    "RollerSki",
    "Rowing",
    "Run",
    "Sail",
    "Skateboard",
    "Snowshoe",
    "Soccer",
    "StairStepper",
    "StandUpPaddling",
    "Surfing",
    "Swim",
    "Velomobile",
    "VirtualRide",
    "Walk",
    "WeightTraining",
    "Wheelchair",
    "Windsurf",
    "Workout",
    "Yoga"
)

class StravaUser:
    """
    Main user class for interacting with Strava's API
    New instance must be created for each user

    >>> Note:
    >>> Due to limitations regarding compatability with Flask Session, new
    >>> instances of stravalib.Client class object needs to be created for
    >>> each method.

    Built upon Hozn's stravalib python library
    """

    ####################################################################################################
    #################################### DEFINE ALL VARIABLES HERE #####################################
    ####################################################################################################
    """
    Variable list:
    - `MY_STRAVA_CLIENT_ID`
        - Methods: Getter
        - Static
    - `MY_STRAVA_CLIENT_SECRET`
        - Methods: Getter
        - Static
    - `access_token`
        - Methods: Getter; Setter
        - Dynamic
    - `refresh_token`
        - Methods: Getter; Setter
        - Dynamic
    - `expires_at`
        - Methods: Getter; Setter
        - Static
    - `firstname`
        - Methods: Getter; Setter
        - Dynamic
    - `lastname`
        - Methods: Getter; Setter
        - Dynamic
    - `weight`
        - Methods: Getter; Setter
        - Dynamic
    - `redirect_url`
        - Methods: Getter; Setter
        - Dynamic
    - `default_gap_days`
        - Methods: Getter
        - Static
    - `activity_list`
        - Methods: Getter; Setter
        - Dynamic
    """


    ###########################
    ### MY_STRAVA_CLIENT_ID ###
    ###########################
    """
    Variable: `MY_STRAVA_CLIENT_ID` (developer's client ID)
    Reference: None
    Methods: Getter
    
    ***Notes***
    This is used to access Strava's API

    In this program, developer's client ID used is Joel C
    """
    
    # Getter method
    @property
    def MY_STRAVA_CLIENT_ID(self):
        # Get currently stored <<<MY_STRAVA_CLIENT_ID>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return 57202
    

    ###############################
    ### MY_STRAVA_CLIENT_SECRET ###
    ###############################
    """
    Variable:  `MY_STRAVA_CLIENT_SECRET` (developer's client secret)
    Reference: None
    Methods: Getter

    ***Notes***
    This is used to access Strava's API

    In this program, developer's client secret used is Joel C
    """

    # Getter method
    @property
    def MY_STRAVA_CLIENT_SECRET(self):
        # Get currently stored <<<MY_STRAVA_CLIENT_SECRET>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return "88a09c5c484f9a31973e51c71a981b8cddd963fa"
    

    ####################
    ### access_token ###
    ####################
    """
    Variable: `access_token`
    Reference: `self.__access_token`
    Methods: Getter; Setter

    ***Notes***
    This is the token that provides access to a specific Strava account
    """

    # Getter method
    @property
    def access_token(self):
        # Get currently stored <<<access_token>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__access_token
    
    # Setter method
    @access_token.setter
    def access_token(self, token):
        # Set <<<access_token>>> to <token>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__access_token = token
    

    #####################
    ### refresh_token ###
    #####################
    """
    Variable: `refresh_token`
    Reference: `self.__refresh_token`
    Methods: Getter; Setter

    ***Notes***
    This is the token that is required to obtain a new access token
    """

    # Getter method
    @property
    def refresh_token(self):
        # Get currently stored <<<refresh_token>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__refresh_token
    
    # Setter Method
    @refresh_token.setter
    def refresh_token(self, token):
        # Set <<<refresh_token>>> to <token>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__refresh_token = token
    

    ##################
    ### expires_at ###
    ##################
    """
    Variable: `expires_at`
    Reference: `self.__expires_at`
    Methods: Getter; Setter

    ***Notes***
    This is the number of seconds since Epoch when the provided access token will expire
    """
    
    # Getter method
    @property
    def expires_at(self):
        # Get currently stored <<<expires_at>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__expires_at
    
    # Setter method
    @expires_at.setter
    def expires_at(self, token):
        # Set <<<expires_at>>> to <token>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__expires_at = token
    

    #################
    ### firstname ###
    #################
    """
    Variable: `firstname`
    Reference: `self.__firstname`
    Methods: Getter; Setter

    ***Notes***
    The current athlete's firstname (as per stored in Strava)
    """
    
    # Getter method
    @property
    def firstname(self):
        # Get currently stored <<<firstname>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__firstname
    
    # Setter method
    @firstname.setter
    def firstname(self, name):
        # Set <<<firstname>>> to <name>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__firstname = name
    

    ################
    ### lastname ###
    ################
    """
    Variable: `lastname`
    Reference: `self.__lastname`
    Methods: Getter; Setter

    ***Notes***
    The current athlete's lastname (as per stored in Strava)
    """
    
    # Getter method
    @property
    def lastname(self):
        # Get currently stored <<<lastname>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__lastname
    
    # Setter method
    @lastname.setter
    def lastname(self, name):
        # Set <<<lastname>>> to <name>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__lastname = name
    

    ##############
    ### weight ###
    ##############
    """
    Variable: `weight`
    Reference: `self.__weight`
    Methods: Getter; Setter

    ***Notes***
    The current athlete's weight (as per stored in Strava)
    """

    # Getter method
    @property
    def weight(self):
        # Get currently stored <<<weight>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__weight
    
    # Setter method
    @weight.setter
    def weight(self, mass):
        # Set <<<weight>>> to <mass>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        # Also ensures that the <<<weight>>> is a float
        try:
            # Try to convert <mass> directly into a float
            self.__weight = float(mass)
        except:
            # If unable to convert directly to float
            # Try to convert using unithelper from Stravalib
            try:
                self.__weight = float(unithelper.kilograms(mass))
            except:
                # If also unable to convert to float, set <<<weight>>> to None
                self.__weight = None
    

    ####################
    ### redirect_url ###
    ####################
    """
    Variable: `redirect_url`
    Reference: `self.__redirect_url`
    Methods: Getter; Setter

    ***Notes***
    This is the url where the user is to be redirected to after authorization
    """
    
    # Getter method
    @property
    def redirect_url(self):
        # Get currently stored <<<redirect_url>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__redirect_url
    
    # Setter method
    @redirect_url.setter
    def redirect_url(self, new_url):
        # Set <<<redirect_url>>> to <new_url>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        try:
            # validators.url() only takes str or byte as param
            # and will throw an exception otherwise
            is_valid = validators.url(new_url)
        except:
            # If it throws an exception, assume url not valid
            is_valid = False
        
        if is_valid == True:
            # If url valid, then set <<<redirect_url>>>
            self.__redirect_url = new_url
        else:
            # If not valid, set default
            self.__redirect_url = 'https://localhost:8080'

    
    ########################
    ### default_gap_days ###
    ########################
    """
    Variable: `default_gap_days`
    Reference: None
    Methods: Getter

    ***Notes***
    The default number of days separating start and end in the timeframe
    """

    # Getter method
    @property
    def default_gap_days(self):
        # Get currently stored <<<default_gap_days>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return 90


    #####################
    ### activity_list ###
    #####################
    """
    Variable: `activity_list`
    Reference: `self.__activity_list`
    Methods: Getter; Setter

    ***Notes***
    An array of activity variables
    """

    # Getter method
    @property
    def activity_list(self):
        # Get currently stored <<<activity_list>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__activity_list
    
    # Setter method
    @activity_list.setter
    def activity_list(self, new_list):
        # Set <<<activity_list>>> to <new_list>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")

        # Ensure that <new_list> is a list (array)
        correct_type = True
        if isinstance(new_list, list) is False:
            correct_type = False
        else:
            # If <new_list> is a list, check each item is of type dict
            for item in new_list:
                if isinstance(item, dict) is False:
                    correct_type = False
                # Do nothing if of type dict
        
        if correct_type is True:
            # Set <<<activity_list>>> to <new_list> if correct type
            self.__activity_list = new_list
        else:
            # Otherwise set <<<activity_list>>> to None
            self.__activity_list = None
    
    #######################
    ### start_time_list ###
    #######################
    """
    Variable: `start_time_list`
    Reference: `self.__start_time_list`
    Methods: Getter; Setter

    ***Notes***
    An array of activity start times (as time.struct_time objects)
    """

    # Getter method
    @property
    def start_time_list(self):
        # Get currently stored <<<start_time_list>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__start_time_list
    
    # Setter method
    @start_time_list.setter
    def start_time_list(self, new_list):
        # Set <<<start_time_list>>> to <new_list>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")

        # Set correct type to False
        # Only changes to True if <new_list> is an array with correct element types
        correct_type = False

        # Check <new_list> is an array
        if isinstance(new_list, list):
            # Set correct type to True
            # Changes to False if any element is not of type struct_time
            correct_type = True
            for element in new_list:
                # Loop through to ensure all elements are correct type
                if isinstance(element, time.struct_time) is False:
                    correct_type = False
        
        if correct_type is True:
            # Set <<<activity_list>>> to <new_list> if correct type
            self.__start_time_list = new_list
        else:
            # Otherwise set <<<activity_list>>> to None
            self.__start_time_list = None
    

    ####################################################################################################
    ########################################## CLASS METHODS ###########################################
    ####################################################################################################

    #######################
    ### Private Methods ###
    #######################

    def __init__(self, 
                 access_token=None, 
                 refresh_token=None, 
                 expires_at=None):
        """
        Initialise a new user object.

        :param access_token: The token that provides access to a specific Strava account.
                             If empty, assume authorization required. (Default is `None`)
        :type access_token: str

        :param refresh_token: The token that is required to obtain a new access token.
                              If empty, assume authorization required. (Default is `None`)
        :type refresh_token: str

        :param expires_at: The number of seconds since Epoch when the provided access.
                           token will expire. (Default is `None`)
        :type expires_at: str
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Set access_token, refresh_token and expires_at
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

        # Set all other *dynamic variables* to None
        self.firstname = None
        self.lastname = None
        self.weight = None
        self.redirect_url = None
        self.activity_list = None
        self.start_time_list = None

        try:
            # All 3 parameters required for successful class creation without authorization
            # Check if latest access token has expired, and update if ncessary
            self.__check_expiry()
        except:
            # For all other cases, authorization is required again
            pass
    
    def __new_client_instance(self):
        """
        Makes a new instance of `stravalib.Client` object.

        :return: A :class:`stravalib.Client` object to manipulate.
        :rtype: :class:`stravalib.Client`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        if self.access_token is not None:
            client = Client(access_token=self.access_token)
        else:
            client = Client()
        return client
    
    def __check_expiry(self):
        """
        Checks the access token expiry against current time. Must execute 
        before any action.
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Get new access token if current time is past expiry time
        if time.time() > self.expires_at:
            self.__refresh_access_token()
    
    def __refresh_access_token(self):
        """
        Generate access token using currently stored refresh token.
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        if self.access_token is None: # Ensures that old access token still exists
            raise Exception("Permission Error")
        
        # Create new instance of Client class object
        client = self.__new_client_instance()

        # Get refresh response
        refresh_response = client.refresh_access_token(
            client_id=self.MY_STRAVA_CLIENT_ID,
            client_secret=self.MY_STRAVA_CLIENT_SECRET,
            refresh_token=self.refresh_token
        )

        # Update short-lived access token
        self.access_token = refresh_response['access_token']
        # Refresh token to be used later to obtain another valid access token
        self.refresh_token = refresh_response['refresh_token']
        # Access token is only valid for 6 hours, indicates the expiry time
        self.expires_at = refresh_response['expires_at']
    
    def __get_profile_variables(self, athlete_object):
        """
        Set `firstname`, `lastname` and `weight` from an athlete object.
        
        :param athlete_object: The athlete object to get variables from.
        :type athlete_object: :class:`stravalib.model.Athlete`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Set values as per stravalib.model.Athlete object
        self.firstname = athlete_object.firstname
        self.lastname = athlete_object.lastname
        self.weight = athlete_object.weight

    def __make_activity_dict(self, activity_batch):
        """
        Loops through `stravalib.client.BatchedResultsIterator` and gets
        important variables from `stravalib.model.Activity` objects. Also
        extracts start dates from all activities, convert each date into a
        `time.struct_time` object and stores it.

        :param activity_batch: The batch of activities to loop through.
        :type activity_batch: :class:`stravalib.client.BatchedResultsIterator`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Initialise empty arrays
        act_array, start_array = [], []

        for activity in activity_batch:
            # Get attributes of each activity
            activity_attributes = attrs(activity)
            
            # Initialise empty dict
            activity_dict = {}

            # Add attributes to dict of attributes
            # Activity *Name* (already str)
            activity_dict['name'] = activity_attributes['name']
            # Activity *Type*
            activity_dict['type'] = activity_attributes['type']
            # Activity *Distance* (convert to float and round to 2dp)
            activity_dict['distance'] = round(float(unithelper.kilometers(activity_attributes['distance'])), 2)
            # Activity *Moving time* (convert to seconds)
            activity_dict['moving time'] = unithelper.timedelta_to_seconds(activity_attributes['moving_time'])
            # Activity *Elapsed time* (convert to seconds)
            activity_dict['elapsed time'] = unithelper.timedelta_to_seconds(activity_attributes['elapsed_time'])
            # Activity *Start date local* (convert to seconds since Epoch)
            activity_dict['start date local'] = time.mktime(datetime_to_epochsecs(activity_attributes['start_date_local']))
            # Activity *Manual entry* (already boolean)
            activity_dict['manual entry'] = activity_attributes['manual']
            # Activity *Average speed* (convert to float and round to 2dp)
            activity_dict['average speed'] = round(float(unithelper.kilometers_per_hour(activity_attributes['average_speed'])), 2)

            # Add dict of atributes to array
            act_array.append(activity_dict)

            # Convert and append start date
            start_array.append(time.localtime(activity_dict['start date local']))
        
        # Save to `self.activity_list`
        self.activity_list = act_array

        # Save to `self.start_time_list`
        self.start_time_list = start_array
    
    def __make_day_hr(self):
        """
        Extract start dates from all activites, then converts them into
        sub-arrays of day of week and hour. *Note that day of week will
        always precede hour.

        :return: A matrix consisting of the weekday and hour of the start
                 time.
        :rtype: :class:`numpy.ndarray`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Create a local copy of the activity list to work
        activities = self.activity_list

        # Initialise a temporary list to store start dates
        start_dates = []

        # Get start dates from activity list
        for activity in activities:
            start_dates.append(activity["start date local"])
        
        # Convert start dates array to an array of day and hours
        day_hour = to_day_hr_arr(start_dates)
        
        # Convert array of day and hours to a numpy array
        return np.array(day_hour)


    ######################
    ### Public Methods ###
    ######################

    def generate_authorize_url(self, redirect_to="https://localhost:8080"):
        """
        Generates the URL at which the user should authorize.

        :param redirect_to: The url where the user is to be redirected after
                            authorization. (Default is "localhost:8080")
        :type redirect_to: str

        :return: The URL that clients should use to authorize the app.
        :rtype: str
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Create new instance of Client class object
        client = self.__new_client_instance()

        logging.critical(redirect_to)

        # Set redirect_url
        # Will ensure url is valid inside Setter function
        self.redirect_url = redirect_to

        # Check if redirect_url is valid
        url = client.authorization_url(
            client_id=self.MY_STRAVA_CLIENT_ID,
            redirect_uri=self.redirect_url,
            approval_prompt='auto'
        )

        # Redirect to authorizatinon url. 
        # 'Code' parameter will be added to url if authorization is successful
        return url
    
    def authorize_user(self, code):
        """
        Authorize a new user using code from authorization url.

        :param code: A unique code returned from a successful authorization
                     with Strava.
        :type code: str
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Create new instance of Client class object
        client = self.__new_client_instance()

        token_response = client.exchange_code_for_token(
            client_id=self.MY_STRAVA_CLIENT_ID,
            client_secret=self.MY_STRAVA_CLIENT_SECRET,
            code=code
        )

        # Update short-lived access token
        self.access_token = token_response['access_token']
        # Refresh token to be used later to obtain another valid access token
        self.refresh_token = token_response['refresh_token']
        # Access token is only valid for 6 hours, indicates the expiry time
        self.expires_at = token_response['expires_at']
    
    def deauthorize_user(self):
        """
        Deauthorize a user.
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Create new instance of Client class object
        client = self.__new_client_instance()
        client.deauthorize()
    
    def get_strava_profile(self):
        """
        Get user's strava profile to set `firstname`, `lastname` and `weight`.
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Check expiry of access token
        self.__check_expiry()

        # Create new instance of Client class object
        client = self.__new_client_instance()
        
        # Get a stravalib.model.Athlete class object
        # Documentation found here: 
        # https://github.com/hozn/stravalib/blob/eabeabf5b40d818ea7c0d9f0bd6c4d619450581f/stravalib/model.py#L277
        strava_profile = client.get_athlete()
        
        # Only save certain variables from that object
        # Cannot save object directly due to JSON serialization issue
        self.__get_profile_variables(strava_profile)
    
    def get_strava_activities(self, before=None, after=None):
        """
        Get strava activities within a certain timeframe.

        :param before: The time BEFORE which activities will be taken. If `None`
                       (default) then activities will be taken until the current
                       date and time.
        :type before: :class:`datetime.datetime`

        :param after: The time AFTER which activities will be taken. If `None`
                      (default) then activities will be taken within a 90 day 
                      timeframe from `before`.
        :type after: :class:`datetime.datetime`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Set before_time
        if isinstance(before, datetime.datetime):
            # If *before* is a datetime.datetime object (means was provided and is valid)
            before_time = before
        else:
            # If *before* was not provided in param or invalid,
            # Use current date as default
            before_time = datetime.datetime.today()
        
        # Set after_time
        if isinstance(after, datetime.datetime):
            # If *after* is a datetime.datetime object (means was provided and is valid)
            after_time = after
        else:
            # If *after* was not provided in param or invalid,
            # Use before_time - _default_after as default
            after_time = before_time - datetime.timedelta(days=self.default_gap_days)
        
        # Create new instance of Client class object
        client = self.__new_client_instance()

        # Get activities within timeframe
        activities = client.get_activities(before=before_time, after=after_time, limit=None)
        
        # Make into array of dictionary
        self.__make_activity_dict(activities)
    
    def weekly_pattern(self):
        """
        Cluster by start weekday and hour using DBSCAN.

        :return: The :class:`DBSCAN` object fitted to dataset.
        :rtype: :class:`DBSCAN`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Get matrix of start weekday and hour
        day_hr_arr = self.__make_day_hr()

        # Instantiate Clustering object
        cluster = Clustering(dataset=day_hr_arr)

        # Use Cluster object
        cluster.general_DBSCAN()
        
        # Group the clusters
        cluster_groups = cluster.group_clusters()
        
        return cluster_groups
    
    def find_patterns(self, activity_data):
        """
        Attempt to find and identify patterns within the given activity
        data.
        """

        # First try to find any weekly patterns in the data

