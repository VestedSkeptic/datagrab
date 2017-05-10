
# *****************************************************************************
# ADD A CUSTOM LOGGING LEVEL -> logging.TRACE
import logging
logging.TRACE = 9
logging.addLevelName(logging.TRACE, "DEBUGV")

def trace(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(logging.TRACE):
        self._log(logging.TRACE, message, args, **kws)
logging.Logger.trace = trace

# *****************************************************************************
# Update sys.path to allow importing python files from library and script directory
import sys, os
sys.path.insert(0, "/home/delta/work/scriptsPython") # first value is index, setting to zero puts this path in front of existing paths

# *****************************************************************************
# Instantiate logging module
from mLogging import mLogging_init, getmLoggerInstance

consoleLoggingLevel = logging.TRACE

# fileLoggingLevel    = logging.DEBUG
fileLoggingLevel    = logging.TRACE

mLogging_init("django_logger", consoleLoggingLevel, fileLoggingLevel, "out.txt")

logger = getmLoggerInstance()
# logger.debug("sys.path = %s" % sys.path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


logger.trace('trace message')
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')