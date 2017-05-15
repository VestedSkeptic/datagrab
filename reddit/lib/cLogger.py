#!/usr/bin/env python
import logging
import datetime
import time
import inspect
import os
# import pprint

cLoggerLevel_CRITICAL   = logging.CRITICAL
cLoggerLevel_ERROR      = logging.ERROR
cLoggerLevel_WARNING    = logging.WARNING
cLoggerLevel_INFO       = logging.INFO
cLoggerLevel_DEBUG      = logging.DEBUG
cLoggerLevel_TRACE      = 9
cLoggerLevel_NOTSET     = logging.NOTSET

cLoggerArchive_True     = True
cLoggerArchive_False    = False

# *****************************************************************************
class cLogger(object):

    # --------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.baseLoggerLevel        = logging.CRITICAL
        self.handlerLevels          = {}
        self.loggerInfoLevel        = logging.DEBUG
        self.methodInfoLevel        = logging.DEBUG
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.baseLoggerLevel)
        self.funcdict = {}

    # --------------------------------------------------------------------------
    def addConsoleLogger(self, loggingLevel, name):
        handler = logging.StreamHandler()
        handler.setLevel(loggingLevel)
        self.handlerLevels[name]=loggingLevel
        formatter = logging.Formatter(self.getFormatString(), datefmt='%H:%M:%S')
        formatter.converter = time.localtime
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        if loggingLevel < self.baseLoggerLevel:
            self.baseLoggerLevel = loggingLevel
            self.logger.setLevel(self.baseLoggerLevel)

    # --------------------------------------------------------------------------
    def getArchiveFilename(self, fNameKey, archiveIndex, fNameType):
        return "%s%03d.%s" % (fNameKey, archiveIndex, fNameType)

    # --------------------------------------------------------------------------
    def archiveOlderVersions(self, pathFileName):
        # get path and filename
        pathFileTuple = pathFileName.rpartition('/')    # if success: path = pathFileTuple[0], filename = pathFileTuple[2]
        # get fname and ftype
        nameTypeTuple = pathFileTuple[2].partition('.') # if success: fname = nameTypeTuple[0], type = nameTypeTuple[2]

        if not (pathFileTuple[0] and pathFileTuple[1] and nameTypeTuple[0] and nameTypeTuple[1]):
            self.logger.critical("Error splitting %s into path and file and or %s into name and type" % (pathFileName, pathFileTuple[2]))
        else:
            fNameKey    = nameTypeTuple[0]         # if success: fNameKey = element 0
            fNameType   = nameTypeTuple[2]         # if success: fNameType = element 2
            # get names of all previously archived files
            fileList = []
            for fname in os.listdir(pathFileTuple[0]):
                if fname.startswith(fNameKey):
                    fileList.append(fname)
            # remove base filename if in list
            if (pathFileTuple[2] in fileList):
                fileList.remove(pathFileTuple[2])
            # reverse sort fileList
            fileList.sort(reverse=True)
            # len(fileList) = number of archived files found.
            # therefore increment by one for archive_index for renaming
            archiveIndex = len(fileList) + 1
            # fileList is sorted with oldest names first: ex log_004.txt, log_003.txt, log_002.txt, log_001.txt
            # for each rename with older archiveIndex
            for x in fileList:
                archiveFilename = self.getArchiveFilename(fNameKey, archiveIndex, fNameType)
                # self.logger.critical("%s to be renamed to %s" % (x, archiveFilename))
                archiveIndex -= 1
                os.rename(pathFileTuple[0]+'/'+x, pathFileTuple[0]+'/'+archiveFilename)
            # finally rename newest log file
            archiveFilename = self.getArchiveFilename(fNameKey, archiveIndex, fNameType)
            if (os.path.isfile(pathFileName)):
                os.rename(pathFileName, pathFileTuple[0]+'/'+archiveFilename)

    # --------------------------------------------------------------------------
    def addFileLogger(self, pathFileName, loggingLevel, name, archiveType):
        if archiveType==cLoggerArchive_True:
            self.archiveOlderVersions(pathFileName)
        handler = logging.FileHandler(pathFileName, mode='w', encoding=None, delay=False)
        handler.setLevel(loggingLevel)
        self.handlerLevels[name]=loggingLevel
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
        for k in self.handlerLevels:
            mPtr("%-24s: %s" % (k, logging.getLevelName(self.handlerLevels[k])))
        mPtr("%-24s: %s" % ("Logger Info Level", logging.getLevelName(self.loggerInfoLevel)))
        mPtr("%-24s: %s" % ("Method Info Level", logging.getLevelName(self.methodInfoLevel)))
        mPtr("************************************************************")
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
        methodName = inspect.stack()[1][3]
        fileNameWithType = inspect.stack()[1][1].rpartition('/')[2] # right partition string by backslash and return third part of tuple
        fileName = fileNameWithType.partition('.')[0]

        os = "%-20s: " % (fileName + "." + methodName + "()")
        args, _, _, values = inspect.getargvalues(inspect.stack()[1][0])
        firstIteration = True
        for i in args:
            if firstIteration: os += "("
            else: os += ", "
            firstIteration = False
            os += "%s=%s" % (i, values[i])
        if not firstIteration: os += ")"

        # Full methodInfo to TRACE
        mPtr = self.getMethodPtr(cLoggerLevel_TRACE)
        mPtr(os)

        return methodName + "(): "

















