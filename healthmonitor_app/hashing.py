"""
Module for any simplified hashing using Python built-in library *hashlib*
"""

import hashlib, binascii, os

# Set iterations for hash
ITERATIONS = 1000

def hash_item(item):
    """
    Hash an item with a randomly generated salt.

    :param item: The item to hash.
    :type item: str

    :return: The salt and hashed item appended together in a string.
    :rtype: str
    """

    # Generate salt
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')

    # Generate hashed item
    item_hash = hashlib.pbkdf2_hmac('sha512', item.encode('utf-8'), 
                                salt, ITERATIONS)
    
    # Turn hashed item into string
    item_hash = binascii.hexlify(item_hash)
    
    # Append salt and hashed and convert to string
    return (salt + item_hash).decode('ascii')
 
def verify_item(stored_item, provided_item):
    """
    Verify whether a raw item matches with a hashed item.

    :param stored_item: The already hashed item.
    :type stored_item: str

    :param provided_item: The raw item to verify.
    :type provided_item: str

    :return: An indicator whether the items match. `True` if they match
             and `False` if they don't match.
    :rtype: boolean
    """
    
    # Get stored salt
    salt = stored_item[:64]
    # Get stored item
    stored_item = stored_item[64:]
    
    # Generate hash for given item
    item_hash = hashlib.pbkdf2_hmac('sha512', provided_item.encode('utf-8'), 
                                  salt.encode('ascii'), ITERATIONS)
    # Turn new hash into string
    item_hash = binascii.hexlify(item_hash).decode('ascii')
    
    # Return an evaluation whether the items match
    return item_hash == stored_item
