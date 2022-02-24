## @package mcs.MowBotControl
# The main system controller for the mowbot

## @file MowBotControl.py
# This file is the main file for the mowbot.
# This is the entry point of the program. use "sudo python3 -m mcs.MowBotControl" to start this file and the robot.
# It spawn all the system controllers and even handles some of the threads like the blades and the navigation.

# Standard Libaries
import multiprocessing as multiproc
import importlib
import time
import os
import threading

# Load Initial Modules
import mcs.controllers.HMI as HMI
import mcs.Flags as Flags

# System Controller Modules
import mcs.InterruptControl as mcs_ic
import mcs.DriveSysControl as mcs_dsc

# Controller Modules
import mcs.controllers.Navigation as mcs_nav
import mcs.controllers.BladeControl as mcs_blades


# Start HMI and get test number
testNum = HMI.getTestNum()

# Update test flags if test specified
if testNum > 0:
    testFile = "test.routines.test" + str(testNum) + ".Flags"
    Flags = importlib.import_module(testFile)

# Create Debug Info
debugPrefix = "[MowBotControl]"
if Flags.MowBotControl_debug:
    print(debugPrefix + ": process spawned")
    print(debugPrefix + ": process id = " + str(os.getpid()))

# main functions
with multiproc.Manager() as manager:
    globals = manager.dict()

    # Super States
    globals['state1'] = 'startup'
    globals['state2'] = 'waitForRemote'

    # Mowbot Control Status
    globals['testNum'] = testNum
    globals['destLat'] = []
    globals['destLong'] = []
    globals['destinationHeading'] = 0
    globals['headingLock'] = False

    # Manual Drive Speeds
    globals['leftSpeed'] = 0
    globals['rightSpeed'] = 0

    # Blade Control
    globals['bladesOn'] = False

    # Battery Bonitor
    globals['batteryLevel'] = None
    globals['batteryCharging'] = None

    # Object Detection
    globals['forwardClearance'] = 200
    globals['leftTurnClear'] = False
    globals['rightTurnClear'] = False
    globals['avoidanceTurnDirection'] = None
    
    # Collision Detection
    globals['bumper1Pressed'] = False
    globals['bumper2Pressed'] = False
    globals['bumper3Pressed'] = False
    globals['bumper4Pressed'] = False
    globals['bumper5Pressed'] = False
    globals['bumper6Pressed'] = False
    globals['bumper7Pressed'] = False

    # Gps Data
    globals['lon'] = -1
    globals['lat'] = -1
    globals['heading'] = -1
    
    # Start Interrupt Controller Process
    proc_ic = multiproc.Process(target = mcs_ic.run, args = (globals, ))
    proc_ic.start()
        
    # Start Drive System Controller Process
    proc_DriveSysControl = multiproc.Process(target = mcs_dsc.run, args = (globals, ))
    proc_DriveSysControl.start()
 
    # Start Navigation Thread
    if Flags.Navigation_enabled:
        thread_navigation = threading.Thread(target = mcs_nav.run, args = (globals, ))
        thread_navigation.start()
    elif Flags.MowBotControl_debug:
        print(debugPrefix + ": Navigation Controller is disabled")

    # start Blade Control Thread
    if Flags.BladeControl_enabled:
        thread_bladeControl = threading.Thread(target = mcs_blades.run, args = (globals, ))
        thread_bladeControl.start()
    elif Flags.MowBotControl_debug:
        print(debugPrefix + ": Blade Control Controller is disabled")

    # Start Program if remote controller not used
    if Flags.DriveSysControl_enabled or not Flags.RemoteControl_enabled:
        time.sleep(3)
        globals['state1'] = 'mow'

    # Stall until Shutdown Loop
    while globals['state1'] != 'shutdown':
        time.sleep(2)
    
    globals['bladesOn'] = False

    # Wait for threads to end
    if Flags.BladeControl_enabled:
        thread_bladeControl.join()
    
    if Flags.Navigation_enabled:
        thread_navigation.join()
    
    # wait for processes to end
    proc_ic.join()
    proc_DriveSysControl.join()

if Flags.MowBotControl_debug:
    print(debugPrefix + ": end of program")