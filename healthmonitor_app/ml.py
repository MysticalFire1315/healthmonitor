"""
ML Element
"""

#from ProgramFiles.CustomPackages.utility import test
import logging, inspect, sys, numpy, math
from typing import Type
import time, datetime

from sklearn.cluster import DBSCAN

# Import other custom modules
from .utility import ensure_type_same, arrdict_to_2darray, make_dict, extract_dayofweek
from .utility import associate_arrays


class Dataset:
    """
    Object to store dataset in
    Provides methods to clean dataset and apply ML algorithms
    """

    ####################################################################################################
    #################################### DEFINE ALL VARIABLES HERE #####################################
    ####################################################################################################

    ###############
    ### dataset ###
    ###############
    """
    Variable: `dataset`
    Reference: `self.__dataset`
    Methods: Getter; Setter
    """
    
    # Getter method
    @property
    def dataset(self):
        # Get currently stored <<<dataset>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__dataset
    
    # Setter method
    @dataset.setter
    def dataset(self, sample):
        # Set <<<dataset>>> to <sample>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        if isinstance(sample, (list, numpy.ndarray)):
            # Ensures that <<<dataset>>> is a list or a numpy array
            self.__dataset = sample
        else:
            raise TypeError('Dataset must be of type `list` or `numpy.ndarray`')
    
    ##############
    ### labels ###
    ##############
    """
    Variable: `labels`
    Reference: `self.__labels`
    Methods: Getter; Setter
    """

    # Getter method
    @property
    def labels(self):
        # Get currently stored <<<labels>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__labels

    # Setter method
    @labels.setter
    def labels(self, new_label):
        # Set <<<labels>>> to <new_label>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        if isinstance(new_label, list):
            # Ensures that <<<labels>>> is a list
            self.__labels = new_label
        else:
            raise TypeError('Labels must of type `list`')
    
    ############
    ### dict ###
    ############
    """
    Variable: `dict`
    Reference: `self.__dict`
    Methods: Getter; Setter
    """

    # Getter method
    @property
    def dict(self):
        # Get currently stored <<<dict>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__dict
    
    # Setter method
    @dict.setter
    def dict(self, new_dict):
        # Set <<<dict>>> to <new_dict>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        if isinstance(new_dict, dict):
            # Ensures that <<<dict>>> is a dictionary
            self.__dict = new_dict
        else:
            raise TypeError('Dict must be of type `dict`')


    ####################################################################################################
    ########################################## CLASS METHODS ###########################################
    ####################################################################################################

    #######################
    ### Private Methods ###
    #######################

    def __init__(self, dataset=[]):
        """
        Initialise a new dataset object

        Param: `dataset`
        Descrip: The dataset to store and manipulate
        Type: `arr`
        Required: False
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Set dataset
        self.dataset = dataset
    
    def __make_int(self, matrix):
        """
        Converts any element in a 2d array to `int` or `float`

        Param: `matrix`
        Descrip: The array to work with
        Type: 2d `arr`
        Required: True

        Return: `dict` & `matrix`
        *`dict`: Contains all items that were replaced (dict)
        *`matrix`: The new 2d array containing only `int` or `float`

        ***Note***\n
        Return dict will be of form:
        >>> {
        >>>     index replaced (int) : {
        >>>         original item name (str) : new item (int)
        >>>     }
        >>> }
        """
        logging.info(f"{inspect.stack()[0][3]} method called")
        
        # Initialise a list to store indexs which need to be changed
        replace_index = []

        # Find any index where item is not an int or float
        for index in range(len(matrix[0])):
            if type(matrix[0][index]) not in (int, float):
                # If item is not of type int or float
                replace_index.append(index)
        
        # Initialise a dict to store items replaced
        # Dict format as described in function descrip
        
        # Note this algorithm taken from utility.make_dict
        # Unable to use function directly due to some Python issues
        # Ref: Issue #1

        # Initialise empty dict
        dict = {}

        # Loop through reference array
        for item in replace_index:
            # Assign val to each item in reference array
            dict[item] = {}

        for index in range(len(matrix)):
            # Loop through matrix line by line to replace items
            for replacable in replace_index:
                # Get current item
                cur_item = str(matrix[index][replacable])
                # Check if item that needs replacing is already in dict
                if cur_item in dict[replacable].keys():
                    # If already in dict (given vaue), replace directly with value
                    matrix[index][replacable] = dict[replacable][cur_item]
                else:
                    # If not yet given value, assign value
                    # Default value assigned is current length of dict for index
                    matrix[index][replacable] = len(dict[replacable])
                    dict[replacable][cur_item] = len(dict[replacable])
        
        return dict, matrix
    
    def __to_dict(self, array, ref):
        """
        Converts an array with references to a dictionary

        Param: `array`
        Descrip: The array to convert
        Type: `list` or `numpy.ndarray`
        Required: True

        Param: `ref`
        Descrip: The references used as keys
        Type: `list`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Check if array is a numpy array
        if isinstance(array, numpy.ndarray):
            array = array.tolist()

        return_val = {}
        for index in range(len(array)):
            # Check if item is a list of some form
            if isinstance(array[index], (list)):
                # Convert return_val into a list if not already
                if isinstance(return_val, dict):
                    return_val = []

                # Recursively convert item
                return_val(self.__to_dict(array[index], ref))
            else:
                # Convert directly
                return_val[ref[index]] = array[index]
        return return_val

    ######################
    ### Public Methods ###
    ######################

    def clean(self, dataset=None):
        """
        Clean and ensure that dataset is ready for applying ML algorithms
        
        >>> Details:
        >>> Check what type is provided in `list`
        >>> If each element is not already of type `int` or `float`, 
            assign value to an `int` and store key in `dict`
        >>> Try to arrange dataset into `Numpy` array
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Use currently stored dataset if not provided a new one
        if dataset is None:
            dataset = self.dataset

        # Check each item to ensure all items are of the same type
        if ensure_type_same(dataset) is False:
            raise TypeError('All items in list must be of same type')
        
        # Convert each item in dataset to array
        # And save labels and reassign dataset
        self.labels, dataset = arrdict_to_2darray(dataset)

        # Convert all items in dataset to int or float
        # Also get dict of items that changed to int or float
        self.dict, dataset = self.__make_int(dataset)

        # Convert items in dataset to tuple to prevent accidental sorting
        for index in range(len(dataset)):
            dataset[index] = tuple(dataset[index])

        # Reassign self.dataset
        self.dataset = numpy.array(dataset)

        print("Labels\n", self.labels)
        print("Dict\n", self.dict)
        print("Dataset\n", self.dataset)

    

    def cluster_times_in_week(self):
        pass


class Clustering:
    """
    A class for appplying a variety of clustering algorithms to various
    usecases. Although this class can be instantiated without a dataset,
    most methods will require a valid dataset.
    
    Employs algorithms from :class:`sklearn.cluster`; further
    documentation for sklearn available at: 
    https://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster

    Currently available algorithms include:
        - DBSCAN
    """

    ####################################################################################################
    #################################### DEFINE ALL VARIABLES HERE #####################################
    ####################################################################################################

    ###############
    ### dataset ###
    ###############
    """
    Variable: `dataset`
    Reference: `self.__dataset`
    Methods: Getter; Setter

    ***Notes***
    The dataset that will be used for any ML algorithms
    """
    
    # Getter method
    @property
    def dataset(self):
        # Get currently stored <<<dataset>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__dataset

    # Setter method
    @dataset.setter
    def dataset(self, new):
        # Set <<<dataset>>> to <new>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        
        if isinstance(new, (numpy.ndarray, type(None))):
            # Save <new> if of type numpy.ndarray or None
            self.__dataset = new
        elif isinstance(new, list):
            # Convert into a numpy array
            self.__dataset = numpy.array(new)
        else:
            # Raise error if not a numpy array, list or None
            raise TypeError('Must be of type numpy.ndarray, list or None')
    
    #############
    ### model ###
    #############
    """
    Variable: `model`
    Reference: `self.__model`
    Methods: Getter; Setter

    ***Notes***
    The return object from any ML algorithms
    """

    # Getter method
    @property
    def model(self):
        # Get currently stored <<<model>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return self.__model
    
    # Setter method
    @model.setter
    def model(self, new_model):
        # Set <<<model>>> to <new_model>
        logging.debug(f"{inspect.stack()[0][3]} setter method called")
        self.__model = new_model
    
    ###############
    ### min_pct ###
    ###############
    """
    Variable: `min_pct`
    Reference: None
    Methods: Getter

    ***Notes***
    Minimum percentage of values to be considered a cluster.
    """

    # Getter method
    @property
    def min_pct(self):
        # Get currently stored <<<min_pct>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return 0.5
    
    ####################
    ### weeks_recent ###
    ####################
    """
    Variable: `weeks_recent`
    Reference: None
    Methods: Getter

    ***Notes***
    Number of weeks considered "recent".
    """

    # Getter method
    @property
    def weeks_recent(self):
        # Get currently stored <<<weeks_recent>>>
        logging.debug(f"{inspect.stack()[0][3]} getter method called")
        return 4


    ####################################################################################################
    ########################################## CLASS METHODS ###########################################
    ####################################################################################################

    #######################
    ### Private Methods ###
    #######################

    def __init__(self, dataset=None):
        """
        Initialise a new Clustering object.

        :param dataset: The dataset to work with. (Defaults to None)
        :type dataset: :class:`list` OR :class:`numpy.ndarray`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Set dataset
        self.dataset = dataset

    def __remove_outliers(self, labels):
        """
        Remove the outliers (-1) from a set of labels generated by sklearn's
        algorithms.

        :param labels: The labels generated by sklearn's algorithm. Should be a numpy
                       array of integers greater or equal to -1.
        :type labels: :class:`numpy.ndarray`

        :return: The labels provided after all -1 has been removed.
        :rtype: :class:`numpy.ndarray`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # First loop through labels to identify indices with -1 as values
        to_be_removed = []
        for index in range(len(labels)):
            if labels[index] == -1:
                to_be_removed.append(index)
        
        return numpy.delete(labels, to_be_removed)
    
    def __check_input_dataset(self, dataset):
        """
        Ensure that the input parameter `dataset` is a list or :class:`numpy.ndarray`,
        otherwise try using instance's `dataset` variable.

        :param dataset: The dataset parameter from a higher level function.
        :type dataset: Any (Should be :class:`list` or :class:`numpy.ndarray`)

        :return: The dataset parameter (or instance's variable) of type 
                 :class:`numpy.ndarray`.
        :rtype: :class:`numpy.ndarray`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")
        
        # Check if dataset parameter is a list
        if isinstance(dataset, list):
            # Convert to numpy array
            return numpy.array(dataset)
        
        # Do nothing if dataset parameter is already a numpy array
        elif isinstance(dataset, numpy.ndarray):
            return dataset
        
        # Otherwise use instance's dataset and check if a numpy array
        elif isinstance(self.dataset, numpy.ndarray):
            return self.dataset
        
        # Dataset parameter not a list or numpy array, and instance's dataset is None
        else:
            # Raise error
            raise TypeError("""`Dataset` not provided or of incorrect type; and 
                                instance's `Dataset` cannot be set to None.""")
    
    def __check_input_model(self, model):
        """
        Ensure that the input parameter `model` is a :class:`sklearn.cluster` object,
        otherwise try using instance's `model` variable. **Note: Currently only able
        to determine that `model` is not None, cannot determine specific type.**

        :param model: The model parameter from a higher level function.
        :type model: Any (Should be a :class:`sklearn.cluster` object)

        :return: The dataset parameter (or instance's variable) of one of
                 :class:`sklearn.cluster`.
        :rtype: :class:`sklearn.cluster`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")
        
        # Check model parameter is not None type
        if isinstance(model, type(None)) is False:
            return model
        
        # Otherwise use instance's model and check not None type
        elif isinstance(self.model, type(None)) is False:
            return self.model
        
        # model parameter is None, and instance's dataset is None
        else:
            # Raise error
            raise TypeError("`Model` and instance's `Model` cannot be None.")

    def __timestamps_to_datetime(self, timestamps):
        """
        Convert a timestamp to :class:`datetime.datetime` form. Original
        timestamp can be of types `int`, `float`, `time.struct_time`,
        `datetime.datetime`, or `list`. If input timestamp is a list, use
        recursion to convert each element in the list to `datetime` form.

        :param timestamps: The timestamp in one of the acceptable forms.
        :type timestamps: various

        :return: Either the individual timestamp or list of timestamps
                 with all elements converted to datetime.
        :rtype: :class:`datetime.datetime` or :class:`list`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # 1. Ensure timestamp is of correct type
        # 2. Otherwise convert into datetime objects

        # Identify element type
        if isinstance(timestamps, (int, float)):
            # If element is an integer, assume that it is using the
            # Seconds since Epoch representation

            # Replace old element with converted element
            timestamps = datetime.datetime.fromtimestamp(
                                    timestamps
                                )
        
        elif isinstance(timestamps, time.struct_time):
            # If element is a struct_time object, convert to int
            # (Seconds since Epoch) then into datetime
            timestamps = datetime.datetime.fromtimestamp(
                                    time.mktime(timestamps)
                                )
        
        elif isinstance(timestamps, datetime.datetime):
            # If element is a datetime object, ignore
            pass

        elif isinstance(timestamps, list):
            # If timestamps is a list, loop through elements and try to
            # convert by recursion
            for index in range(len(timestamps)):
                timestamps[index] = self.__timestamps_to_datetime(
                                                        timestamps[index]
                                                    )
        
        else:
            # If element is not one of the specified types, raise error
            raise TypeError(f"""Timestamp  must be one of the specified
                                types (`int`, `float`, `time.struct_time`,
                                `datetime.datetime`, or `list`).
                            """)

        return timestamps

    def __timestamp_patterns(self, timestamps, max_period=1):
        """
        Attempt to identify any patterns in some timestamps. All timestamps
        must be :class:`datetime.datetime` objects.

        :param timestamps: A list of timestamps, where each element is of type
                           :class:`datetime.datetime`, from which to find
                           patterns.
        :type timestamps: list

        :param max_period: The maximum length of a repeating period. Must be
                           between 1 and days between the first and last
                           timestamps. (Default 1)
        :type max_period: int

        :return: The length of a repeating period where clusters can be found at
                 index 0; and the labels corresponding to each element of the
                 dataset to indicate the presence of a cluster at index 1.
        :rtype: tuple
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Try to convert all timestamps to datetime
        # Does nothing if already of type datetime
        self.__timestamps_to_datetime(timestamps)

        # Calculate the interval between first and last timestamps
        # ie Last - Earliest
        time_interval = max(timestamps) - min(timestamps)

        # Max period length cannot exceed length max interval or less than 1
        if max_period < 1 or time_interval.days < max_period:
            raise ValueError("""Maximum length of a repeating period cannot be
                                less than 1 or greater than the number of
                                days between the first and last timestamps.""")
        
        # `num` is the length of a repeating period to search for clusters in
        # ie. `num` = 7 means weekly
        for num in range(1, 31):
            # Empty array of hours
            hour_array = []
            # Add contents
            for element in timestamps:
                # Index 0 => Day in period (If period is 7, then which weekday)
                # Index 1 => Hour in day (minutes as decimal)
                hour_array.append([
                    element.timetuple().tm_yday % num,
                    element.hour + element.minute/60
                ])
            

            # Cluster timestamps with array of hours

            # `min_points` is the number of periods in the interval between the
            # first and last timestamps
            cluster = self.general_DBSCAN(
                dataset=numpy.array(hour_array),
                min_points=math.floor((time_interval.days /num) * self.min_pct)
            )

            # Check number of clusters
            if self.num_clusters(cluster) > 0:
                # Cluster was identified
                return num, cluster.labels_.tolist()
        
        raise IndexError("No clusters found in specified maximum period length.")
    
    def __time_lengths_to_seconds(self, time_lengths):
        """
        Convert a time length to seconds since epoch form. Original time
        length can be of types `int`, `float`, `datetime.timedelta`, `list`.
        If input time length is a list, use recursion to convert each element
        in the list to Seconds since Epoch form.

        :param time_lengths: The time length in one of the acceptable forms.
        :type time_lengths: various

        :return: Either the individual time period or list of time periods
                 with all elements converted to seconds.
        :rtype: float or list
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # 1. Ensure time length is of correct type
        # 2. Otherwise convert into timedelta objects

        # Identify element type
        if isinstance(time_lengths, (int, float)):
            # If element is an integer or float, convert to float
            time_lengths = float(time_lengths)
        
        elif isinstance(time_lengths, datetime.timedelta):
            # If element is a timedelta object, convert to seconds
            time_lengths = time_lengths.total_seconds()

        elif isinstance(time_lengths, list):
            # If time length is a list, loop through elements and try to
            # convert by recursion
            for index in range(len(time_lengths)):
                time_lengths[index] = self.__time_lengths_to_seconds(
                                                        time_lengths[index]
                                                    )
        
        else:
            # If element is not one of the specified types, raise error
            raise TypeError(f"""Time length  must be one of the specified
                                types (`int`, `float`, `datetime.timedelta`
                                or `list`).
                            """)

        return time_lengths
    
    def __time_length_patterns(self, timestamp_length, max_period):
        """
        Attempt to identify any patterns in some timestamps associated with a length
        of time. Similar to :func:`__timestamp_patterns` except a time length is
        taken into account.

        :param timestamp_length: A list of [timestamp, length of time], where each
                                 timestamp is a :class:`datetime.datetime` object and
                                 length of time a representation of Seconds Since Epoch,
                                 from which to find patterns.
        :type timestamp_length: list

        :param max_period: The maximum length of a repeating period. Must be
                           between 1 and days between the first and last
                           timestamps. (Default 1)
        :type max_period: int

        :return: The length of a repeating period where clusters can be found at
                 index 0; and the labels corresponding to each element of the
                 dataset to indicate the presence of a cluster at index 1.
        :rtype: tuple
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Calculate the interval between first and last timestamps
        # ie Last - Earliest
        # max and min functions use first item in each subarray
        time_interval = max(timestamp_length) - min(timestamp_length)

        # Max period length cannot exceed length max interval or less than 1
        if max_period < 1 or time_interval.days < max_period:
            raise ValueError("""Maximum length of a repeating period cannot be
                                less than 1 or greater than the number of
                                days between the first and last timestamps.""")

        # `num` is the length of a repeating period to search for clusters in
        # ie. `num` = 7 means weekly
        for num in range(1, max_period):
            # Empty array of hours
            hour_array = []
            # Add contents
            for element in timestamp_length:
                # Index 0 => Day in period (If period is 7, then which weekday)
                # Index 1 => Length of time
                hour_array.append([
                    element[0].timetuple().tm_yday % num,
                    element[1]
                ])
            
            # Cluster timestamps with array of hours

            # `min_points` is the number of periods in the interval between the
            # first and last timestamps
            cluster = self.general_DBSCAN(
                dataset=numpy.array(hour_array),
                min_points=math.floor((time_interval.days /num) * self.min_pct)
            )

            # Check number of clusters
            if self.num_clusters(cluster) > 0:
                # Cluster was identified
                return num, cluster.labels_.tolist()
        
        raise IndexError("No clusters found in specified maximum period length.")
    

    ######################
    ### Public Methods ###
    ######################

    def general_DBSCAN(self, dataset=None, max_dist=0.5, min_points=3):
        """
        For generic usecases. Identifies clusters within a dataset using
        scikit-learn's DBSCAN algorithm. Also store the :class:`sklearn.cluster.DBSCAN`
        object in instance's :var:`cluster` variable. Further information available at:
        https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html

        :param dataset: The dataset to cluster. If None, use instance's :var:`dataset`.
                        (Default is None)
        :type dataset: list or :class:`numpy.ndarray`

        :param max_dist: The maximum distance between two points for them to be
                         considered within the same group. (Default is 0.5)
        :type max_dist: float

        :param min_points: The minimum number of points in a group for the group to
                           be considered a cluster. (Default is 3)
        :type min_points: int

        :return: An instance of :class:`sklearn.cluster.DBSCAN` fitted to the dataset
                 provided or currently stored in the current object instance.
        :rtype: :class:`sklearn.cluster.DBSCAN`
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Check dataset input parameter is valid or use instance's
        dataset = self.__check_input_dataset(dataset)

        # Fit dataset to instance of DBSCAN
        self.model = DBSCAN(eps=max_dist, min_samples=min_points).fit(dataset)

        # Return instance of DBSCAN
        return self.model
    
    def group_clusters(self, dataset=None, labels=None, model=None):
        """
        Group clusters identified by one of the clustering algorithms. Returns an
        array containing identified groups in subarrays. Input options include the
        labels already in an array or the entire `sklearn.cluster` object. Note that
        if a list of labels is provided, this algorithm will prioritise using it.

        :param dataset: The original dataset clustered. If None, use instance's
                        :var:`dataset`. (Default is None)
        :type dataset: list or :class:`numpy.ndarray`

        :param labels: A list integers indicating the location of any clusters, where
                       -1 points to an outlier, and >= 0 is a cluster group. The
                       length of the list must be the same as the length of the
                       original dataset. If None, use input parameter `model` instead.
                       (Default is None)
        :type labels: list

        :param model: The sklearn clustering model returned after fitting some data to
                      a ML algorithm. If None, use instance's :var:`model`. (Default
                      is None)
        :type model: An object from :module:`sklearn.cluster`

        :return: An array containing the identified cluster groups in subarrays.
        :rtype: list
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Check dataset input parameter is valid or use instance's
        # Note that this means that dataset will be a numpy array
        dataset = self.__check_input_dataset(dataset)

        # Check if labels parameter is None
        if labels is None:
            # If labels was not provided, get labels from model

            # Check model input parameter is valid or use instance's
            model = self.__check_input_model(model)

            # Require Try/Except block in case cluster used is not an object
            # from sklearn (ie. doesn't have required attributes such as labels_)
            try:
                # Get labels indicating which cluster each element belongs to
                labels = model.labels_
            except:
                # model was not a sklearn object
                raise TypeError("""Input parameter `model` or instance's variable
                                   `model` was not a `sklearn.cluster` object.""")
        
        else:
            # If labels was provided, check to ensure that all labels are
            # integers >= -1
            for label in labels:
                if label < -1:
                    raise ValueError("All labels must be <= 0.")

        # Create an dictionary to store labels along with coresponding items
        grouped = {}
        
        # Loop through labels to group clusters
        for index in range(len(labels)):
            # Check if labels is already in dictionary
            if labels[index] not in grouped.keys():
                # Add label to dictionary, along with corresponding item
                grouped[labels[index]] = [dataset[index]]
            else:
                # Append corresponding item to dictionary at correct label
                grouped[labels[index]].append(dataset[index])
        
        # Once dictionary has been filled, extract any labels that are not -1
        to_return = []
        # Loop through to find any labels not -1
        for label in grouped.keys():
            # If the label is > -1 (means not an outlier)
            if label > -1:
                # Add to the array to return
                to_return.append(grouped[label])
        
        return to_return
    
    def num_clusters(self, model=None):
        """
        Identify the number of clusters within a given sklearn clustering
        model.

        :param model: The sklearn clustering model from which to infer the number of
                      clusters. If None, use instance's :var:`model`. (Default is
                      None)
        :type model: An object from :module:`sklearn.cluster`

        :return: The number of cluster groups within the clustering model.
        :rtype: int
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Check model input parameter is valid or use instance's
        model = self.__check_input_model(model)

        # Get the labels from model
        labels = model.labels_

        # -1 = outlier, and clusters are numbered based on which group
        # they belong to
        # Therefore num of clusters = max in labels + 1
        return max(labels) +1
    
    def cluster_timestamps(self, timestamps):
        """
        Cluster an array of timestamps and identify how these clusters occur.
        
        Timestamps can be of types:
        - :class:`int` / :class:`float`  => Seconds since Epoch representation;
                                            consult :func:`time.gmtime(0)` for the
                                            exact time.
        - :class:`time.struct_time`      => Tuple representation of time value, as
                                            returned by functions such as
                                            :func:`time.gmtime()` and 
                                            :func:`time.localtime()`.
        - :class:`datetime.datetime`     => A representation of time similar to
                                            :class:`time.struct_time`.
        
        :param timestamps: A list of timestamps to cluster. These timestamps can be
                           of a variety of types.
        :type timestamps: list

        :return: A tuple containing the length of the repeating period the clusters
                 were found in (eg. 7 means repeating weekly) at index 0; and a list
                 of any clusters that were identified (clusters in sub lists) at
                 index 1. Note that if the period is 0 and the list is empty, that
                 means no clusters were found.
        :rtype: tuple
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Convert all timestamps to datetime format
        timestamps = self.__timestamps_to_datetime(timestamps)


        # Try to identify time patterns
        try:
            period, labels = self.__timestamp_patterns(timestamps, 31)
        except:
            # If no patterns in the entire timeframe can be detected,
            # Attempt to detect patterns in a more recent timeframe

            # Set earliest possible date (using weeks_recent)
            earliest_allowed = max(timestamps) - datetime.timedelta(days=2)
            
            # Only use timestamps after earliest_allowed
            to_remove = []
            for index in range(len(timestamps)):
                # Loop through to get index of timestamps before allowed date
                if timestamps[index] < earliest_allowed:
                    to_remove.append(index)
            
            # Delete those index (go backwards as to not interfere with indexing)
            to_remove.sort(reverse=True)
            for item in to_remove:
                del timestamps[item]
            
            # Try to identify patterns
            try:
                period, labels = self.__timestamp_patterns(timestamps, 31)
            except:
                # No patterns identified even in recent timeframe
                # Set period to 0 and leave labels as an empty array
                period, labels = 0, []
        
        # Check if any clusters were identified. If so, find their original
        # timestamps and group in an array

        # Clusters were identified if period > 0
        if period > 0:
            # Use the group clusters method
            clusters = self.group_clusters(dataset=timestamps, labels=labels)
        else:
            clusters = []
        
        # Return period and clusters
        return period, clusters

    def cluster_time_lengths(self, timestamps, time_lengths):
        """
        Cluster an array of time lengths, assuming that each index in the time
        length list is associated with the identical index in the timestamp list,
        and identify how these clusters occur. 
        
        Timestamps can be of types:
        - :class:`int` / :class:`float`  => Seconds since Epoch representation;
                                            consult :func:`time.gmtime(0)` for the
                                            exact time.
        - :class:`time.struct_time`      => Tuple representation of time value, as
                                            returned by functions such as
                                            :func:`time.gmtime()` and 
                                            :func:`time.localtime()`.
        - :class:`datetime.datetime`     => A representation of time similar to
                                            :class:`time.struct_time`.

        Time lengths can be of types:
        - :class:`int` / :class:`float`  => Seconds between start and end.
        - :class:`datetime.timedelta`    => Tuple representation of time value.
        
        :param timestamps: A list of timestamps that correspond to the time lengths.
                           These timestamps can be of a variety of types.
        :type timestamps: list

        :param time_lengths: A list of time lengths that correspond to the timestamps,
                             used to identify clusters. These time lengths can be of a
                             variety of types.
        :type time_lengths: list

        :return: A tuple containing the length of the repeating period the clusters
                 were found in (eg. 7 means repeating weekly) at index 0; and a list
                 of any clusters that were identified (clusters in sub lists) at
                 index 1. Note that if the period is 0 and the list is empty, that
                 means no clusters were found.
        :rtype: tuple
        """
        logging.info(f"{inspect.stack()[0][3]} method called")

        # Convert all timestamps to datetime format
        timestamps = self.__timestamps_to_datetime(timestamps)

        # Convert all time lengths to seconds
        time_lengths = self.__time_lengths_to_seconds(time_lengths)

        # Combine timestamps and time lengths
        combined = associate_arrays(timestamps, time_lengths)

        # Try to identify patterns across entire timeframe
        try:
            period, labels = self.__time_length_patterns(combined, 31)
        except:
            # If no patterns in the entire timeframe can be detected,
            # Attempt to detect patterns in a more recent timeframe

            # Set earliest possible date (using weeks_recent)
            earliest_allowed = max(timestamps) - datetime.timedelta(days=2)
            
            # Only use timestamps after earliest_allowed
            to_remove = []
            for index in range(len(combined)):
                # Loop through to get index of timestamps before allowed date
                if combined[index][0] < earliest_allowed:
                    to_remove.append(index)
            
            # Delete those index (go backwards as to not interfere with indexing)
            to_remove.sort(reverse=True)
            for item in to_remove:
                del timestamps[item]
            
            # Try to identify patterns
            try:
                period, labels = self.__time_length_patterns(combined, 31)
            except:
                # No patterns identified even in recent timeframe
                # Set period to 0 and leave labels as an empty array
                period, labels = 0, []
        
        # Check if any clusters were identified. If so, find their original
        # index in the combined array and group in an array

        # Clusters were identified if period > 0
        if period > 0:
            # Use the group clusters method
            clusters = self.group_clusters(dataset=combined, labels=labels)
        else:
            clusters = []
        
        # Return period and clusters
        return period, clusters
    
    

if __name__ == "__main__":
    # Test Data
    test_data = [
        datetime.datetime(2021, 7, 25, 6, 30, 36), 
        datetime.datetime(2021, 7, 24, 4, 31, 20), 
        datetime.datetime(2021, 7, 18, 6, 32, 48), 
        datetime.datetime(2021, 7, 17, 4, 29, 33), 
        datetime.datetime(2021, 7, 10, 4, 20, 59), 
        datetime.datetime(2021, 7, 4, 6, 33, 38), 
        datetime.datetime(2021, 7, 3, 4, 30, 7), 
        datetime.datetime(2021, 6, 27, 6, 24, 7), 
        datetime.datetime(2021, 6, 26, 4, 29, 9), 
        datetime.datetime(2021, 7, 15, 6, 26, 10), 
        datetime.datetime(2021, 7, 19, 4, 30), 
        datetime.datetime(2021, 7, 2, 6, 9, 32), 
        datetime.datetime(2021, 6, 30, 9, 0), 
        datetime.datetime(2021, 6, 25, 16, 1, 9), 
        datetime.datetime(2021, 6, 19, 4, 30), 
        datetime.datetime(2021, 6, 18, 13, 53, 6), 
        datetime.datetime(2021, 6, 15, 11, 32, 18), 
        datetime.datetime(2021, 6, 5, 4, 30), 
        datetime.datetime(2021, 6, 2, 12, 53, 59), 
        datetime.datetime(2021, 5, 29, 4, 30), 
        datetime.datetime(2021, 5, 23, 6, 15, 8), 
        datetime.datetime(2021, 5, 22, 4, 30), 
        datetime.datetime(2021, 5, 17, 16, 33, 11), 
        datetime.datetime(2021, 5, 16, 6, 14, 21), 
        datetime.datetime(2021, 5, 15, 4, 30), 
        datetime.datetime(2021, 5, 15, 4, 10, 41), 
        datetime.datetime(2021, 5, 9, 6, 13, 39), 
        datetime.datetime(2021, 5, 7, 14, 52, 53), 
        datetime.datetime(2021, 5, 7, 5, 47, 51), 
        datetime.datetime(2021, 5, 2, 6, 11, 6), 
        datetime.datetime(2021, 5, 1, 6, 20, 13)]

    cluster = Clustering()
    period, cluster_groups = cluster.cluster_timestamps(test_data)
    print(period)
    print('\n\n')
    print(cluster_groups)