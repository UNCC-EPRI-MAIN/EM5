import os
import time
import importlib

def run(testNum):

    # load test flags
    import mcs.test_flags as tFlags
    if testNum > 0:
        testFile = "test.routines.test" + str(testNum) + ".test_flags"
        print(testFile)
        tFlags = importlib.import_module(testFile)

    debug = tFlags.dsc_debug
    enabled = tFlags.dsc_enabled
    debugPrefix = "[DriveSysCont]"
    if tFlags.dsc_over:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"
    if debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))

    print("------------------------------test drive------")

    print(debugPrefix + ": end of function")
