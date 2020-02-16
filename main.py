import logging

from datatype import DataType
from db import db
from parse import parse

logger = logging.getLogger('ini_converter')
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler('ini_converter.log')
fileHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)

configFiles = ['test.ini']
test = db()
test.buildTables()

for path in configFiles:
    logger.info('parsing ' + path)
    modelData, addresses, relays = parse(path)

    logger.info('inserting data from ' + path)
    test.insert(DataType.MODEL, modelData)
    test.insert(DataType.ADDRESS, addresses)
    test.insert(DataType.RELAY, relays)
