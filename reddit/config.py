import cLogger

clog = None

# --------------------------------------------------------------------------
def initializeCLogger():
    global clog
    # clog = cLogger.cLogger("WorkingLogger")
    clog = cLogger.cLogger(__name__)
    clog.addTraceLoggingLevel()
    clog.generateFuncDict()
    clog.addConsoleLogger(cLogger.cLoggerLevel_INFO, "hConsole",  cLogger.cLoggerFilter_None)

    clog.addFileLogger("/home/delta/work/logs/out.txt",   cLogger.cLoggerLevel_DEBUG,   "hFile out",    cLogger.cLoggerFile_archiveOlder,     cLogger.cLoggerFilter_None)
    clog.addFileLogger("/home/delta/work/logs/trace.txt", cLogger.cLoggerLevel_TRACE,   "hFile trace",  cLogger.cLoggerFile_overwriteOlder,   cLogger.cLoggerFilter_SpecificLevelOnly)
    clog.addFileLogger("/home/delta/work/logs/alert.txt", cLogger.cLoggerLevel_WARNING, "hFile alert",  cLogger.cLoggerFile_appendOlder,      cLogger.cLoggerFilter_GreaterThanOrEqualToLevel)

    clog.setLoggerInfoLevel(cLogger.cLoggerLevel_TRACE)
    clog.setMethodInfoLevel(cLogger.cLoggerLevel_DEBUG)
    clog.dumpLoggerInfo()












