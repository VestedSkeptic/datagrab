# *****************************************************************************
# Update sys.path to allow importing python files from libPython directory
import sys
sys.path.insert(0, "/home/delta/work/mysite2/reddit/lib")

# *****************************************************************************
# Set up logger
from reddit.config import initializeCLogger
initializeCLogger()



