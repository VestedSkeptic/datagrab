#!/usr/bin/env python
import logging
import datetime
import time
import inspect
import pprint

cLoggerLevel_CRITICAL   = logging.CRITICAL
cLoggerLevel_ERROR      = logging.ERROR
cLoggerLevel_WARNING    = logging.WARNING
cLoggerLevel_INFO       = logging.INFO
cLoggerLevel_DEBUG      = logging.DEBUG
cLoggerLevel_TRACE      = 9
cLoggerLevel_NOTSET     = logging.NOTSET

# *****************************************************************************
class cLogger(object):

    # --------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.baseLoggerLevel        = logging.CRITICAL
        self.consoleHandlerLevel    = logging.NOTSET
        self.fileHandlerLevel       = logging.NOTSET
        self.loggerInfoLevel        = logging.DEBUG
        self.methodInfoLevel        = logging.DEBUG
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.baseLoggerLevel)
        self.funcdict = {}

    # --------------------------------------------------------------------------
    def addConsoleLogger(self, loggingLevel):
        handler = logging.StreamHandler()
        handler.setLevel(loggingLevel)
        self.consoleHandlerLevel= loggingLevel
        formatter = logging.Formatter(self.getFormatString(), datefmt='%H:%M:%S')
        formatter.converter = time.localtime
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if loggingLevel < self.baseLoggerLevel:
            self.baseLoggerLevel = loggingLevel
            self.logger.setLevel(self.baseLoggerLevel)

    # --------------------------------------------------------------------------
    def addFileLogger(self, filePathAndName, loggingLevel):
        handler = logging.FileHandler(filePathAndName, mode='w', encoding=None, delay=False)
        handler.setLevel(loggingLevel)
        self.fileHandlerLevel= loggingLevel
        formatter = logging.Formatter(self.getFormatString(), datefmt='%H:%M:%S')
        formatter.converter = time.localtime
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if loggingLevel < self.baseLoggerLevel:
            self.baseLoggerLevel = loggingLevel
            self.logger.setLevel(self.baseLoggerLevel)

    # --------------------------------------------------------------------------
    def addTraceLoggingLevel(self):
        logging.TRACE = cLoggerLevel_TRACE
        logging.addLevelName(logging.TRACE, "TRACE")
        def trace(self, message, *args, **kws):
            if self.isEnabledFor(logging.TRACE):
                self._log(logging.TRACE, message, args, **kws)
        logging.Logger.trace = trace

    # --------------------------------------------------------------------------
    def generateFuncDict(self):
        self.funcdict['CRITICAL']   = self.logger.critical
        self.funcdict['ERROR']      = self.logger.error
        self.funcdict['WARNING']    = self.logger.warning
        self.funcdict['INFO']       = self.logger.info
        self.funcdict['DEBUG']      = self.logger.debug
        self.funcdict['TRACE']      = self.logger.trace

    # --------------------------------------------------------------------------
    # ref: https://docs.python.org/2/library/logging.html#logrecord-attributes
    # %(levelname).1s has a precision of 1 so that many characters
    def getFormatString(self):
        return '%(asctime)-8s %(levelname).1s %(filename)-18s (line %(lineno)4s): %(message)s'

    # --------------------------------------------------------------------------
    def getMethodPtr(self, loggingLevel):
        methodPtr = self.funcdict[logging.getLevelName(loggingLevel)]
        return methodPtr

    # --------------------------------------------------------------------------
    def setLoggerInfoLevel(self, loggingLevel):
        self.loggerInfoLevel = loggingLevel

    # --------------------------------------------------------------------------
    def setMethodInfoLevel(self, loggingLevel):
        self.methodInfoLevel = loggingLevel

    # --------------------------------------------------------------------------
    def dumpLoggerInfo(self):
        mPtr = self.getMethodPtr(self.loggerInfoLevel)
        now = datetime.datetime.now()
        mPtr("************************************************************")
        mPtr("%-24s: %s" % ("Initialized", self.name))
        mPtr("%-24s: %s" % ("Time", str(now)))
        mPtr("%-24s: %s" % ("Base Logger Level", logging.getLevelName(self.baseLoggerLevel)))
        mPtr("%-24s: %s" % ("Console Handler Level", logging.getLevelName(self.consoleHandlerLevel)))
        mPtr("%-24s: %s" % ("File Handler Level", logging.getLevelName(self.fileHandlerLevel)))
        mPtr("%-24s: %s" % ("Logger Info Level", logging.getLevelName(self.loggerInfoLevel)))
        mPtr("%-24s: %s" % ("Method Info Level", logging.getLevelName(self.methodInfoLevel)))
        mPtr("************************************************************")
        mPtr("")
        return

    # --------------------------------------------------------------------------
    # inspect.stack()[1]    is parent of current or what called methodTrace.
    # (
    #     <frame object at 0x7fcc7718e228>,
    #     '/media/shared/work/mysite2/reddit/vbase.py',
    #     7,
    #     'main',
    #     ['    config.clog.methodTrace()\n'],
    #     0
    # )
    # inspect.stack()[1][0]
    def dumpMethodInfo(self):
        mPtr = self.getMethodPtr(self.methodInfoLevel)
        methodName = inspect.stack()[1][3]
        fileName = inspect.stack()[1][1].rpartition('/')[2] # right partition string by backslash and return third part of tuple

        mPtr("-------------------------------------")
        mPtr("%-15s: %s" % ("FileName", fileName))
        mPtr("%-15s: %s" % ("MethodName", methodName))
        args, _, _, values = inspect.getargvalues(inspect.stack()[1][0])
        for i in args:
            mPtr("%-15s: %s" % (i, values[i]))

        # return fileName + " - " + methodName + "(): "
        return methodName + "(): "

















