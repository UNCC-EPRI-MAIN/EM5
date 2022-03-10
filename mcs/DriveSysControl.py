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

# Module Parameters
NORMAL_DRIVE_SPEED = 50                     # Speed of the wheels normals
CAUTION_DRIVE_SPEED = 40                    # speed of the wheels when 
OBJECT_DETECTION_SLOW_DOWN_FACTOR = 1.5     # lower number -> more gradual slowdown
OBJECT_DETECTION_STOP_DISTANCE = 15         # cm
PIVOT_SPEED = 18                            # % motor speed
DEGREES_OFF_COURSE = 5                      # threshold to determine MowBot is off course
DEGREES_FORCE_PIVOT = 90                    # number of degrees off course requiring pivot


def slowDownSpeed(distance):
    # reached stop distance
    if distance < OBJECT_DETECTION_STOP_DISTANCE:
        speed = 0
    else:
        speed = int(OBJECT_DETECTION_SLOW_DOWN_FACTOR * (distance - OBJECT_DETECTION_STOP_DISTANCE))

    if speed > NORMAL_DRIVE_SPEED:
        speed = NORMAL_DRIVE_SPEED

    if speed < 0:
        speed = 0

    return speed

def run(globals):
    
    # main loop, wait for shutdown
    while globals['state1'] != 'shutdown':
        time.sleep(2)
