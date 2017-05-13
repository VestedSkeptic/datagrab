# *****************************************************************************
# Update sys.path to allow importing python files from libPython directory
import sys
sys.path.insert(0, "/home/delta/work/libPython")

# *****************************************************************************
# Set up logger
import reddit.config
import cLogger

reddit.config.clog = cLogger.cLogger("WorkingLogger")
reddit.config.clog.addTraceLoggingLevel()
reddit.config.clog.generateFuncDict()
reddit.config.clog.addConsoleLogger(cLogger.cLoggerLevel_INFO)
reddit.config.clog.addFileLogger("log.txt", cLogger.cLoggerLevel_TRACE)
reddit.config.clog.dumpLoggerInfo()
reddit.config.clog.setLoggerInfoLevel(cLogger.cLoggerLevel_INFO)
reddit.config.clog.setMethodInfoLevel(cLogger.cLoggerLevel_TRACE)


