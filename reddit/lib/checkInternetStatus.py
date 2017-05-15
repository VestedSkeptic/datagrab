#!/usr/bin/env python
import requests
import argparse
import time
# import os
# import sys
# import pprint

CONST_CONTINUE              = 0
CONST_FINI_SUCCESS          = 1
CONST_FINI_KEYBOARD_QUIT    = 2

# *****************************************************************************
def doRequestToUrl(url, count, verbose):
    processingStatus = CONST_CONTINUE

    try:
        r = requests.get(url)
        processingStatus = CONST_FINI_SUCCESS
    except KeyboardInterrupt:
        processingStatus = CONST_FINI_KEYBOARD_QUIT
    except:
        if verbose:
            print ("*** Try  #%d to url %s failed." % (count, url))
        else:
            print ("*** Try #%d failed." % (count))

    return processingStatus

# *****************************************************************************
def parseCommandLineArguments():

    parser = argparse.ArgumentParser()

    # --------------------
    # Positional arguments
    # args.url
    parser.add_argument("url", help="URL to test");

    # type and valid choices specified
    # args.iterations
    parser.add_argument("iterations", help="number of iterations to test. 0 = run forever.", type=int);

    # --------------------
    # Optional arguments

    # Both -v and --verbose acceptable
    # if specified then args.verbose will equal true otherwise false
    # args.verbose
    parser.add_argument("-v", "--verbose", help="verbosity of output message", action="store_true");

    # Different way to specify option arguments
    # args.signage
    # allows input = -d  -> args.delay = 1
    # allows input = -dd  -> args.delay = 2
    # allows input = -ddd  -> args.delay = 3
    # default value if argument not provided
    parser.add_argument("-d", "--delay", help="delay in seconds between tests", action="count", default=0);

    args = parser.parse_args()

    print ("")
    print ("args.url = %s" %(args.url))
    print ("args.iterations = %d" %(args.iterations))
    print ("args.verbose = %s" %(args.verbose))
    print ("args.delay = %d" %(args.delay))

    return args


# *****************************************************************************
# url               ex http://www.example.com
# verbose           True or False
# iterations        int, 0 = forever
# delay             int, seconds, 0 = no delay
def checkInternet(url, verbose, iterations, delay):
    print("===================")

    processingStatus = CONST_CONTINUE
    count = 1
    while processingStatus == CONST_CONTINUE:
        processingStatus = doRequestToUrl(url, count, verbose);
        if iterations > 0 and count >= iterations:
            print("Fini: %d iterations tested" % (iterations))
            break
        count += 1

        if delay > 0 and processingStatus == CONST_CONTINUE:
            time.sleep(delay)


    if processingStatus == CONST_FINI_SUCCESS:
        print("=================== success")
    elif processingStatus == CONST_FINI_KEYBOARD_QUIT:
        print("=================== keyboard quit")





# *****************************************************************************
if __name__ == "__main__":
    args = parseCommandLineArguments()
    checkInternet(args.url, args.verbose, args.iterations, args.delay)



















