import logging

def initLogging(phonenumber):
    logging.basicConfig(filename=phonenumber+'.log', level=logging.INFO)
    logging.basicConfig(filename=phonenumber+'.log', level=logging.DEBUG)
    logging.basicConfig(filename=phonenumber+'.log', level=logging.ERROR)

def print_and_logging(message):
    print(message)
    logging.info(message)