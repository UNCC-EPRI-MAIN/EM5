

# standard libraries
import os
import importlib
import threading
import time

def run(globals):

    # load initial globals
    testNum = globals['testNum']
  
    # load test flags
    import mcs.testFlags as tFlags
    if testNum > 0:
        testFile = "test.routines.test" + str(testNum) + ".testFlags"
        print(testFile)
        tFlags = importlib.import_module(testFile)

    # create debug info
    debug = tFlags.InterruptControl_debug
    enabled = tFlags.InterruptControl_enabled
    debugPrefix = "[InterruptCont]"
    if tFlags.InterruptControl_over:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"  
    if debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))

    # load collision detection controller
    if tFlags.CollisionDetection_over:
        testDir = "test.routines.test" + str(testNum) + ".CollisionDetection"
        CollisionDetection = importlib.import_module(testDir)
    else:
        import mcs.controllers.CollisionDetection as CollisionDetection
    # start collision detection thread
    if enabled:
        thread_collisionDetection = threading.Thread(target = CollisionDetection.run, args = (globals, ))
        thread_collisionDetection.start()

    # load object dection
    if tFlags.rpLiDAR_A2M4_R4_over:
        testDir = "test.routines.test" + str(testNum) + ".rpLiDAR_A2M4_R4"
        rpLiDAR_A2M4_R4 = importlib.import_module(testDir)
    else:
        import mcs.firmware.rpLiDAR_A2M4_R4 as rpLiDAR_A2M4_R4
    # start object detection thread
    if enabled:
        lidar = rpLiDAR_A2M4_R4.rpLiDAR_A2M4_R4(tFlags.rpLiDAR_A2M4_R4_debug, tFlags.rpLiDAR_A2M4_R4_enabled, tFlags.rpLiDAR_A2M4_R4_over)
        thread_objectDetection = threading.Thread(target = lidar.objectDetection, args = (globals, ))
        thread_objectDetection.start()

    # main loop, wait for shutdown
    while globals['state1'] != 'shutdown':
        time.sleep(2)

    # wait for threads to end
    if enabled:
        thread_objectDetection.join()
        thread_collisionDetection.join()

    print(debugPrefix + ": end of process")