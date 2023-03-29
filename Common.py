import logging

def initLogging(phonenumber):
    logging.basicConfig(filename=phonenumber+'.log', level=logging.INFO)

def print_and_logging(message):
    print(message)
    logging.info(message)