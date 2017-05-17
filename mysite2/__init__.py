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
reddit.config.clog.addConsoleLogger(cLogger.cLoggerLevel_INFO, "hConsole",  cLogger.cLoggerFilter_None)

reddit.config.clog.addFileLogger("/home/delta/work/logs/out.txt",   cLogger.cLoggerLevel_DEBUG,   "hFile out",    cLogger.cLoggerFile_archiveOlder,     cLogger.cLoggerFilter_None)
reddit.config.clog.addFileLogger("/home/delta/work/logs/trace.txt", cLogger.cLoggerLevel_TRACE,   "hFile trace",  cLogger.cLoggerFile_overwriteOlder,   cLogger.cLoggerFilter_SpecificLevelOnly)
reddit.config.clog.addFileLogger("/home/delta/work/logs/alert.txt", cLogger.cLoggerLevel_WARNING, "hFile alert",  cLogger.cLoggerFile_appendOlder,      cLogger.cLoggerFilter_GreaterThanOrEqualToLevel)

reddit.config.clog.setLoggerInfoLevel(cLogger.cLoggerLevel_TRACE)
reddit.config.clog.setMethodInfoLevel(cLogger.cLoggerLevel_DEBUG)
reddit.config.clog.dumpLoggerInfo()




