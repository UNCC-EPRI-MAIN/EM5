## @package mcs.DriveSysControl
# A system controller to control how the mowbot moves

## @file DriveSysControl.py
# Handles the movement of the robot by controlling the speed of the wheel and rotation of the robot.
# NOTE: This has some internal code that interfaces with the motors. Look through the code.

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

    if Flags.RemoteControl_enabled:
        thread_remoteControl = threading.Thread(target = RemoteControl.run, args = (globals, ))
        thread_remoteControl.start()
    elif Flags.DriveSysControl_debug:
        print(debugPrefix + ": Remote Control is disabled")

    # main loop, wait for shutdown
    while globals['state'] != 'shutdown':

        # Slow the robot down when the camera sees a object.
        if globals['blocked'] == True:
            globals['driveState'] = 'cautionstraight'
        
        # No problem with the path.
        else:
            globals['driveState'] = 'straight'

        # Found a object within threshold or the robot is off course
        if globals['objectclose'] == True:
            ## Length of the robot in cm
            LENGTH_OF_ROBOT = 30

            ## Angle of rotation
            pivot_angle = globals['degrees']

            ## CW or CCW
            next_pivot_type = None

            # First Pivot
            if globals['pivot'] == 'cw':
                next_pivot_type = 'ccw'
                globals['driveState'] = 'pivotRight'

            elif globals['pivot'] == 'ccw':
                next_pivot_type = 'cw'
                globals['driveState'] = 'pivotLeft'

            # Wait until the first pivot is done.
            while globals['driveState'] != 'completed':
                time.sleep(1)

            globals['distance'] = LENGTH_OF_ROBOT
            globals['driveState'] = 'straightDistance'

            # Wait until the driving striaght is done.
            while globals['driveState'] != 'completed':
                time.sleep(1)

            

        # If the robot is offcourse according to the GPS
        if globals['offcourse'] == True:
            if globals['pivot'] == 'cw':
                globals['driveState'] = 'pivotRight'

            elif globals['pivot'] == 'ccw':
                globals['driveState'] = 'pivotLeft'

            # Wait until the pivot is done.
            while globals['driveState'] != 'completed':
                time.sleep(2)

            globals['driveState'] = 'straight'
        
        time.sleep(1)

    if Flags.DriveControl_enabled:
        thread_drivecontrol.join()

    print(debugPrefix + ": end of process")
