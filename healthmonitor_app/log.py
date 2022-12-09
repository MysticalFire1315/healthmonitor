import logging, os

# Name of file to write logs to
LOG_FILENAME = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'record.log')

# Set logging configuration
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,
                    format=f"%(asctime)s %(levelname)s : %(message)s")