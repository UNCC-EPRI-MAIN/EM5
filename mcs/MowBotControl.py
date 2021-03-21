## @package mcs.MowBotControl
# Primary process for mcs. 
#
# This file is an auxillary file used to assign GPIO pin assignments for various purposes.
# This file ensures pin numbers do not conflict and provides a mechanism for quick changes.
# All pin numbers use BCM mode. See Raspberry Pi GPIO for more information.
# @author Keith
# @note 03/19/2021: Updated documentation -KS

# standard libaries
import multiprocessing as multiproc
import importlib
import time
import os
import threading

# load initial modules
import mcs.testFlags as tFlags
import mcs.pinAssignments as pins

# start HMI and get test number
# temporarily disabled
#import mcs.controllers.HMI as HMI
#testNum = HMI.getTestNum()
testNum = 0 # normal mode

# update test flags if test specified
if testNum > 0:
    testFile = "test.routines.test" + str(testNum) + ".testFlags"
    print(testFile)
    tFlags = importlib.import_module(testFile)

# create debug info
debug = tFlags.MowBotControl_debug
enabled = tFlags.MowBotControl_enabled
debugPrefix = "[MowBotControl]"
if tFlags.InterruptControl_over:
    debugPrefix += "[O]"
if enabled:
    debugPrefix += "[E]" 
if debug:
    print(debugPrefix + ": process spawned")
    print(debugPrefix + ": process id = " + str(os.getpid()))

# main functions
with multiproc.Manager() as manager: 
    globals = manager.dict() 
    # Super States
    globals['state1'] = 'startup'
    globals['state2'] = 'waitForRemote'

    # mowbot control status
    globals['testNum'] = testNum
    globals['destLat'] = []
    globals['destLong'] = []
    globals['destinationHeading'] = 0
    globals['headingLock'] = False

    # manual drive speeds
    globals['leftSpeed'] = 0
    globals['rightSpeed'] = 0

    # blade control
    globals['bladesOn'] = False

    # interrupt controller statuses
    # battery monitor
    globals['batteryLevel'] = None
    globals['batteryCharging'] = None
    # object detection
    globals['forwardClearance'] = 200
    globals['leftTurnClear'] = False
    globals['rightTurnClear'] = False
    globals['avoidanceTurnDirection'] = None
    
    # collision detection
    globals['bumper1Pressed'] = False
    globals['bumper2Pressed'] = False
    globals['bumper3Pressed'] = False
    globals['bumper4Pressed'] = False
    globals['bumper5Pressed'] = False
    globals['bumper6Pressed'] = False
    globals['bumper7Pressed'] = False

    # gps data
    globals['lon'] = -1
    globals['lat'] = -1
    globals['heading'] = -1


    # load interrupt controller
    if tFlags.InterruptControl_over:
        testDir = "test.routines.test" + str(testNum) + ".InterruptControl"
        mcs_ic = importlib.import_module(testDir)
    else:
        import mcs.InterruptControl as mcs_ic
    # start interrupt controller process
    proc_ic = multiproc.Process(target = mcs_ic.run, args = (globals, ))
    proc_ic.start()

    # load drive system controller
    if tFlags.DriveSysControl_over:
        testDir = "test.routines.test" + str(testNum) + ".DriveSysControl"
        mcs_dsc = importlib.import_module(testDir)
    else:
        import mcs.DriveSysControl as mcs_dsc
    # start drive system controller process
    proc_DriveSysControl = multiproc.Process(target = mcs_dsc.run, args = (globals, ))
    proc_DriveSysControl.start()

    # load Navigation module
    if tFlags.Navigation_over:
        testDir = "test.routines.test" + str(testNum) + ".Navigation"
        Navigation = importlib.import_module(testDir)
    else:
        import mcs.controllers.Navigation as Navigation
    # start GPS thread
    if enabled:
        thread_navigation = threading.Thread(target = Navigation.run, args = (globals, ))
        thread_navigation.start()

    # load blade control module
    if tFlags.BladeControl_over:
        testDir = "test.routines.test" + str(testNum) + ".BladeControl"
        NEO_M8P = importlib.import_module(testDir)
    else:
        import mcs.controllers.BladeControl as BladeControl
    # start blade control thread
    if enabled:
        thread_bladeControl = threading.Thread(target = BladeControl.run, args = (globals, ))
        thread_bladeControl.start()

    # start program if remote controller not used
    if not tFlags.DriveSysControl_enabled or not tFlags.RemoteControl_enabled:
        time.sleep(3)
        globals['state1'] = mow

    # main loop
    while globals['state1'] != 'shutdown':
        time.sleep(2)
    
    globals['bladesOn'] = False

    # wait for threads to end
    if enabled:
        thread_navigation.join()
        thread_bladeControl.join()
    
    # wait for processes to end
    proc_ic.join()
    proc_DriveSysControl.join()

if debug:
    print(debugPrefix + ": end of program")