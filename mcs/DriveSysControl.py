## @package mcs.DriveSysControl
# A system controller to control how the mowbot moves

## @file DriveSysControl.py
# Handles the movement of the robot by controlling the speed of the wheel and rotation of the robot.
# NOTE: This has some internal code that directly interfaces with the motors. Look through the code.

# standard libaries
import os
import time
import importlib
import threading

# Controller Modules
import mcs.controllers.DriveControl as DriveControl
import mcs.controllers.RemoteControl as RemoteControl

def run(globals):
    
    flagpath = globals['flagFile']
    Flags = importlib.import_module(flagpath)

    # Create debug info
    debugPrefix = "[DriveSysControl]"
    if Flags.DriveSysControl_enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"
        
    if Flags.DriveSysControl_debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))

    # start drive control thread
    if Flags.DriveControl_enabled:
        thread_drivecontrol = threading.Thread(target = DriveControl.run, args = (globals, ))
        thread_drivecontrol.start()
    elif Flags.DriveSysControl_debug:
        print(debugPrefix + ": Drive Control is disabled")

    # main loop, wait for shutdown
    while globals['state'] != 'shutdown':
        time.sleep(2)

    if Flags.DriveControl_enabled:
        thread_drivecontrol.join()

    print(debugPrefix + ": end of process")
