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
import mcs.controllers.MessageHandler as mcs_message
import mcs.controllers.LidarController as mcs_lidar

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

    # start message handler thread.
    if Flags.MessageHandler_enabled:
        thread_messagehandler = threading.Thread(target = mcs_message.run, args = (globals, ))
        thread_messagehandler.start()
    elif Flags.InterruptControl_debug:
        print(debugPrefix + ": Message Handler Controller is disabled")

    # start object detection thread
    if Flags.Lidar_enabled:
        thread_lidar = threading.Thread(target = mcs_lidar.run, args = (globals, ))
        thread_lidar.start()
    elif Flags.InterruptControl_debug:
        print(debugPrefix + ": LiDAR firmware is disabled")

    # main loop, wait for shutdown
    while globals['state'] != 'shutdown':
        time.sleep(2)

    # wait for threads to end
    if Flags.Lidar_enabled:
        thread_lidar.join()

    if Flags.CollisionDetection_enabled:
        thread_collisionDetection.join()

    if Flags.MessageHandler_enabled:
        thread_messagehandler.join()

    print(debugPrefix + ": end of process")