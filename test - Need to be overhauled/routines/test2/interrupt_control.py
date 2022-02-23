import os
import importlib

def run(testNum):
    
    # load test flags
    import mcs.test_flags as tFlags
    if testNum > 0:
        testFile = "test.routines.test" + str(testNum) + ".test_flags"
        print(testFile)
        tFlags = importlib.import_module(testFile)

    debug = tFlags.ic_debug
    enabled = tFlags.ic_enabled
    debugPrefix = "[InterruptCont]"
    if tFlags.ic_over:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"  
    if debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))
    
    print("----------------test interupt----------")

    print(debugPrefix + ": end of function")