# *****************************************************************************
# Update sys.path to allow importing python files from libPython directory
import sys
sys.path.insert(0, "/home/delta/work/mysite2/reddit/lib")

# *****************************************************************************
# Set up logger
import reddit.config
import cLogger

reddit.config.clog = cLogger.cLogger("WorkingLogger")
reddit.config.clog.addTraceLoggingLevel()
reddit.config.clog.generateFuncDict()
reddit.config.clog.addConsoleLogger(cLogger.cLoggerLevel_INFO, "hConsole")
reddit.config.clog.addFileLogger("/home/delta/work/mysite2/logs/out.txt", cLogger.cLoggerLevel_DEBUG, "hFile out", cLogger.cLoggerArchive_True)
reddit.config.clog.addFileLogger("/home/delta/work/mysite2/logs/trace.txt", cLogger.cLoggerLevel_TRACE, "hFile trace", cLogger.cLoggerArchive_False)
reddit.config.clog.setLoggerInfoLevel(cLogger.cLoggerLevel_INFO)
reddit.config.clog.setMethodInfoLevel(cLogger.cLoggerLevel_TRACE)
reddit.config.clog.dumpLoggerInfo()




