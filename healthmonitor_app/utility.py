import inspect, types, collections, time, math
import numpy as np


def month_to_words(month):
    """
    Converts an integer representation of month to words (first 3 letters),
    where 1 = Jan to 12 = Dec.

    :param month: An integer representation of the month to convert.
    :type month: int

    :return: A string representation of the month (first 3 letters).
    :rtype: str
    """

    if month == 1:
        return 'Jan'
    elif month == 2:
        return 'Feb'
    elif month == 3:
        return 'Mar'
    elif month == 4:
        return 'Apr'
    elif month == 5:
        return 'May'
    elif month == 6:
        return 'Jun'
    elif month == 7:
        return 'Jul'
    elif month == 8:
        return 'Aug'
    elif month == 9:
        return 'Sep'
    elif month == 10:
        return 'Oct'
    elif month == 11:
        return 'Nov'
    elif month == 12:
        return 'Dec'
    else:
        raise ValueError('Month must be between 1 and 12 inclusive.')

def weekday_to_words(weekday):
    """
    Converts an integer representation of weekday to words (first 3 letters),
    where 0 = Mon to 6 = Sun.

    :param weekday: An integer representation of the weekday to convert.
    :type weekday: int

    :return: A string representation of the weekday (first 3 letters).
    :rtype: str
    """

    if weekday == 0:
        return 'Mon'
    elif weekday == 1:
        return 'Tue'
    elif weekday == 2:
        return 'Wed'
    elif weekday == 3:
        return 'Thu'
    elif weekday == 4:
        return 'Fri'
    elif weekday == 5:
        return 'Sat'
    elif weekday == 6:
        return 'Sun'
    else:
        raise ValueError('Weekday must be between 0 and 6 inclusive.')


def display_time_length(seconds_since_epoch):
    """
    Convert a Seconds since Epoch representation of a time length to a human
    readable string for display. Format of the return string will be as
    follows:
        hour(`int`):min(`int`):sec(`int`)

    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: A human-readable representation of the input time.
    :rtype: str
    """

    # Grab components
    hours = math.floor(seconds_since_epoch / 3600)
    mins = math.floor((seconds_since_epoch % 3600) / 60)
    secs = int((seconds_since_epoch % 60) % 60)

    # Format return string
    return_str = f"{hours:02}:{mins:02}:{secs:02}"

    # Get rid of leading 0s
    while return_str[0] == '0' or return_str[0] == ':':
        return_str = return_str[1:]
    
    return return_str

def display_date(seconds_since_epoch):
    """
    Convert a Seconds since Epoch representation of a time to a human readable
    string for display. Format of the return string will be as follows:
        weekday(`str`), day(`int`)/mon(`int`)/year(`int`)
    
    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: A human-readable representation of the input time.
    :rtype: str
    """
    
    # First convert to struct_time object
    struct_time_obj = time.localtime(seconds_since_epoch)

    # Grab components
    wday = weekday_to_words(struct_time_obj.tm_wday)
    mday = str(struct_time_obj.tm_mday)
    mon = str(struct_time_obj.tm_mon)
    
    # Join to make string
    return_str = wday + ', '
    # Append day
    if len(mday) < 2:
        return_str += '0'
    return_str += mday + '/'
    # Append month
    if len(mon) < 2:
        return_str += '0'
    return_str += mon + '/'
    # Append year
    return_str += str(struct_time_obj.tm_year)

    return return_str




def attrs(obj):
    """
    Get all attributes of an object.

    :param obj: The object to work with.
    :type obj: :class:

    :return: A dictionary containing the attributes as keys and
             attribute values as values.
    :rtype: dict
    """
    disallowed_properties = {
        name for name, value in inspect.getmembers(type(obj)) 
        if isinstance(value, (property, types.FunctionType))}
    return {
        name: getattr(obj, name) for name in api(obj) 
        if name not in disallowed_properties and hasattr(obj, name)}

def api(obj):
    """
    Get all names in an object.

    :param obj: The object to work with.
    :type obj: :class:

    :return: A list of all names in the object.
    :rtype: list
    """
    return [name for name in dir(obj) if name[0] != '_']

def linear_search(list_to_search, item_to_find):
    """
    Perform linear search on the list (single element). Note: From SDD Course
    Specs document.

    :param list_to_search: The list to search in.
    :type list_to_search: list

    :param item_to_find: The item to find.
    :type item_to_find: any

    :return: The index of where the item was found.
    :rtype: int
    """

    # Let i = 1
    index = 0

    # Let FoundIt = False
    found = False

    # Get RequiredName
    to_be_found = item_to_find

    # WHILE FoundIt is false AND i <= number of names
    while found is False and index < len(list_to_search):
        # IF Names(i) = RequiredName THEN
        if list_to_search[index] == to_be_found or (
            to_be_found in list_to_search[index]) or (
            to_be_found in list_to_search[index].values()
            ):
            # Let FoundIt = true
            found = True
        
        # ELSE
        else:
            # i = i + 1
            index += 1
    
    # IF FoundIt THEN
    if found is True:
        return index
    # ELSE
    else:
        raise ValueError


def datetime_to_epochsecs(timeobj):
    """
    Converts a :class:`datetime.datetime` object to seconds
    since Epoch.

    :param timeobj: The datetime object to convert.
    :type timeobj: :class:`datetime.datetime`
    """
    timestamp = timeobj.utctimetuple()
    return timestamp

def find_items_with_key(array, key, location=None):
    """
    Find all items containing a key phrase in an array.

    :param array: The array to look through.
    :type array: list

    :param key: The keyphrase to find.
    :type key: str

    :param location: A dictionary with keys start and end to
                     indicate where the key phrase should be
                     found. (Default is `None`)
    :type location: dict

    :return: A list of all items with the key phrase.
    :rtype: list
    """

    # Initialise an array to store all items to return
    return_data = []
    
    # Loop through all items in array
    for item in array:
        if location is None:
            # If location not specified, just check if key is in item
            if key.lower() in item.lower():
                return_data.append(item)
        else:
            try:
                # Need in a try block in case location specified exceeds length of item

                lower_item = item.lower()
                # If location is specified, check in location for match
                # Check if location start is None or if location end is None
                if location['start'] is None:
                    if key.lower() in lower_item[:location['end']].lower():
                        return_data.append(item)
                elif location['end'] is None:
                    if key.lower() in lower_item[location['start']:].lower():
                        return_data.append(item)
                else:
                    if key.lower() in lower_item[location['start']:location['end']].lower():
                        return_data.append(item)
            except:
                # Do nothing if out of index (item not found)
                pass
    
    return return_data

def find_items_with_value(dictionary, keyword):
    """
    Find all items within a dictionary where the values is the
    same as a key item.

    :param dictionary: The dictionary to work with.
    :type dictionary: dict

    :param keyword: The key item to find.
    :type keyword: :class:

    :return: An indicator whether the key was found. `True` means
             found and `False` means not found.
    :rtype: boolean
    """
    
    # Check if the keyword is a string
    if isinstance(keyword, str):
        for key in dictionary.keys():
            # Check if keys match ignoring capitalisation
            if keyword.lower() == dictionary[key].lower():
                return True
    else:
        for key in dictionary.keys():
            if keyword == dictionary[key]:
                return True
    return False

def find_dicts_with_val(array, keyword):
    """
    Find the dictionaries with keyword inside an array.

    :param array: The array containing dictionaries to look
                  through.
    :type array: list

    :param keyword: The keyword to find.
    :type keyword: str

    :return: An array containing the dictionaries with
             keyword.
    :rtype: list
    """
    return_arr = []
    for item in array:
        if find_items_with_value(item, keyword):
            return_arr.append(item)
    return return_arr

def ensure_type_same(array):
    """
    Ensure that all elements in an array are of the same type.

    :param array: The array to work with.
    :type array: list

    :return: An indicator whether all elements are of the same
             type. `True` means all same type and `False` means
             different types are present.
    :rtype: boolean
    """

    # Get type of first item in array
    item_type = type(array[0])
    for item in array:
        # Compare type of current item to type of first item
        if type(item) is not item_type:
            return False
    return True

def sort_dict_keys(dict_obj):
    """
    Sort a dictionary by key (ascending).

    :param dict_obj: The dictionary to sort.
    :type dict_obj: dict
    
    :return: The sorted dictionary.
    :rtype: dict
    """

    # Convert to a sorted `OrderedDict` item
    od = collections.OrderedDict(sorted(dict_obj.items()))

    # Convert `OrderedDict` item back to dictionary
    return_dict = {}
    for key, val in od.items():
        return_dict[key] = val
    return return_dict

def arrdict_to_2darray(item):
    """
    Convert an array of dictionaries to a 2d array.

    :param item: The array of dictionaries to convert.
    :type item: list (each item must be a dict)

    :return: The keys of each dict, The values in a 2d array
    :rtype: list, list
    """

    # Sort the dictionaries at each index
    for index in range(len(item)):
        item[index] = sort_dict_keys(item[index])

    # Get labels (keys from dict)
    labels = list(item[0].keys())

    return_array = []

    # Loop through all dicts in item
    for index in range(len(item)):
        # Check that labels match first item's
        if list(item[index].keys()) != labels:
            # Raise error if doesn't match
            raise KeyError('All keys must match!')
        
        # Add values to return
        return_array.append(list(item[index].values()))
    
    # Return labels and 2d array separately
    return labels, return_array

def make_dict(ref, val):
    """
    Make a dictionary with keys from a list and the same values.

    :param ref: The reference to assign keys with.
    :type ref: list

    :param val: The temporary value to give each key.
    :type val: :class:

    :return: The dictionary with temporary values
    :rtype: dict
    """
    
    # Initialise empty dict
    dict = {}

    # Loop through reference array
    for item in ref:
        # Assign val to each item in reference array
        dict[item] = val
    
    return dict

def test(dict_obj, key1, key2):
    """
    Make a numpy array from a list of dictionaries
    with some specified keys.

    :param dict_obj: The list of dictionaries to work with.
    :type dict_obj: list

    :param key1:
    """

    return_val = np.array([dict_obj[key1], dict_obj[key2]])

def extract_dayofweek(seconds_since_epoch):
    """
    Extract the day of the week from the number of seconds since
    epoch. Note that the extract will be an integer between 0 to 6
    inclusive, where 0 is Monday and 6 is Sunday.

    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: The day of week as specified.
    :rtype: int
    """

    # Convert the seconds since epoch into a struct_time object
    struct_time_obj = time.localtime(seconds_since_epoch)

    # Return the weekday
    return struct_time_obj[6]

def extract_hour(seconds_since_epoch):
    """
    Extract the hour (mins in decimal) of day from the number of
    seconds since epoch. Note that the extract will be a float
    between 0 to 24.

    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: The hour of day (with minutes as decimals).
    :rtype: float
    """

    # Convert the seconds since epoch into a struct_time object
    struct_time_obj = time.localtime(seconds_since_epoch)

    # Calculate the hour
    hour = struct_time_obj[3] + struct_time_obj[4]/60

    # Return the hour
    return hour

def extract_min(seconds_since_epoch):
    """
    Extract the minute of day from the number of seconds since
    epoch. Note that the extract will be an integer between 0
    and 59. (Seconds will be rounded to the closest integer.)

    :param seconds_since_epoch: The seconds since epoch to convert.
    :type seconds_since_epoch: int

    :return: The minute of hour (Seconds rounded to closest int).
    :rtype: int
    """

    # Convert the seconds since epoch into a struct_time object
    struct_time_obj = time.localtime(seconds_since_epoch)

    # Calculate the min + secs
    min = struct_time_obj[4] + struct_time_obj[5]/60

    # Return the min (rounded)
    return round(min)

def to_day_hr_arr(seconds_array):
    """
    Convert an array of seconds since epoch timestamps into an
    array containing subarrays of form: [day of week, hour]. Note
    that the date will be lost.

    :param seconds_array: An array of seconds since epoch timestamps.
    :type seconds_array: list

    :return: An array with subarrays containing day of week and hour.
    :rtype: list
    """

    # Initialise the array to return
    return_array = []

    # Loop through seconds_array to convert each item
    for item in seconds_array:
        # Append day of week and hour to the array to return
        return_array.append([extract_dayofweek(item), extract_hour(item)])
    
    return return_array

def to_hr_min_arr(seconds_array):
    """
    Converts an array of seconds since epoch timestamps into an
    array containing subarrays of form: [hour, min]. Note that
    the date will be lost.

    :param seconds_array: An array of seconds since epoch timestamps.
    :type seconds_array: list

    :return: An array with subarrays containing hour and min.
    :rtype: list
    """

    # Initialise the array to return
    return_arr = []

    # Loop through seconds_array to convert each item
    for item in seconds_array:
        # Append hour and min to the array to return
        return_arr.append([math.floor(extract_hour(item)),
                           extract_min(item)])
    
    return return_arr

def associate_arrays(array1, array2):
    """
    Associate two different arrays. (Combine into a single array)
    Element 1 in each array will be put together into a subarray,
    and so forth. Note that array1 and array2 must be of the same
    element length.

    :param array1: The first array. Note that elements from this
                   array will be placed first in the combined array.
    :type array1: list

    :param array2: The second array. Note that elements from this
                   array will be placed second in the combined array.
    :type array2: list

    :return: The combined array.
    :rtype: list
    """

    # Compare length of arrays
    if len(array1) != len(array2):
        raise IndexError("Arrays must be of the same length.")

    # Initialise the array to return
    return_arr = []

    # Loop through to combine arrays
    for index in range(len(array1)):
        return_arr.append([array1[index], array2[index]])
    
    return return_arr