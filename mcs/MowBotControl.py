## @package mcs.MowBotControl
# The main system controller for the mowbot

## @file MowBotControl.py
# The main file for the mowbot.
# This is the entry point of the program. use "sudo python3 -m mcs.MowBotControl" to start this file and the robot.
# It spawn all the system controllers and even handles some of the threads like the blades and the navigation.

# Standard Libaries
import multiprocessing as multiproc
import time
import os
import threading
import importlib

# Load Initial Modules
import RPi.GPIO as GPIO
import mcs.controllers.HMI as HMI
import mcs.Flags as Flags

# System Controller Modules
import mcs.InterruptControl as mcs_ic
import mcs.DriveSysControl as mcs_dsc

# Controller Modules
import mcs.controllers.Navigation as mcs_nav
import mcs.controllers.BladeControl as mcs_blades

GPIO.setmode(GPIO.BCM)

# Start HMI and get test number
testNum = HMI.getTestNum()

# Update test flags
if testNum > 0:
    flagFile = "tests.test" + str(testNum) + ".Flags"
    Flags = importlib.import_module(flagFile)
else:
    flagFile = "mcs.Flags"

# Create Debug Info
debugPrefix = "[MowBotControl]"
if Flags.MowBotControl_debug:
    print(debugPrefix + ": process spawned")
    print(debugPrefix + ": process id = " + str(os.getpid()))

# main functions
with multiproc.Manager() as manager:
    globals = manager.dict()

    # Super States
    if not Flags.RemoteControl_enabled:
        globals['state'] = 'startup'
    else:
        globals['state'] = 'waitForRemote'

    # Mowbot Control Status
    globals['flagFile'] = flagFile
    globals['driveState'] = 'stop'

    # Drive settings
    globals['leftSpeed'] = 0
    globals['rightSpeed'] = 0
    globals['distance'] = 0
    globals['degrees'] = 0
    globals['pivot'] = 'cw'

    # Blade Control
    globals['bladesOn'] = False

    # Object Detection
    globals['objectclose'] = False
    globals['blocked'] = False

    # GPS
    globals['offcourse'] = False
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
    if not Flags.RemoteControl_enabled:
        globals['state'] = 'mow'

    # Stall until Shutdown Loop
    while globals['state'] != 'shutdown':
        time.sleep(2)
    
    # Shutdown the blades and wheels
    globals['driveState'] = 'stop'
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