## @package mcs.InterruptControl
# A system controller to stop the mowbot in a event.

## @file InterruptControl.py
# Tells the robot what to do when a collision happens or theres a object in the way.
# This uses the sensors accelerometer, bumpers, lidar, and the camera.

# standard libraries
import os
import importlib
import threading
import time

# Controller Modules
import mcs.controllers.CollisionDetection as mcs_colldec

# Firmware Modules
import mcs.firmware.rpLiDAR_A2M4_R4 as mcs_lidar

def run(globals):

    flagpath = globals['flagFile']
    Flags = importlib.import_module(flagpath)

    # Create debug info
    debugPrefix = "[InterruptController]"
    if Flags.InterruptControl_enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"  
    if Flags.InterruptControl_debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))
        
    # start collision detection thread
    if Flags.CollisionDetection_enabled:
        thread_collisionDetection = threading.Thread(target = mcs_colldec.run, args = (globals, ))
        thread_collisionDetection.start()
    elif Flags.InterruptControl_debug:
        print(debugPrefix + ": Collision Detection Controller is disabled")

    # At a later date, we will move this in a object detection controller. 
    # start object detection thread
    if Flags.rpLiDAR_A2M4_R4_enabled:
        lidar = mcs_lidar.rpLiDAR_A2M4_R4(Flags.rpLiDAR_A2M4_R4_debug, Flags.rpLiDAR_A2M4_R4_enabled, Flags.rpLiDAR_A2M4_R4_over)
        thread_objectDetection = threading.Thread(target = lidar.objectDetection, args = (globals, ))
        thread_objectDetection.start()
    elif Flags.InterruptControl_debug:
        print(debugPrefix + ": LiDAR firmware is disabled")

    # main loop, wait for shutdown
    while globals['state1'] != 'shutdown':
        time.sleep(2)

    # wait for threads to end
    if Flags.CollisionDetection_enabled:
        thread_objectDetection.join()

    if Flags.rpLiDAR_A2M4_R4_enabled:
        thread_collisionDetection.join()

    print(debugPrefix + ": end of process")