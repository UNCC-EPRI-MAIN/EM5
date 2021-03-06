# ----------------------RPLidar Functions----------------------
#$ pip install rplidar-roboticia


from cmath import exp
import time
from dis import dis
import enum
from statistics import variance
from turtle import distance
from rplidar import RPLidar
from itertools import chain
from math import floor
import importlib

#lidar = RPLidar('COM4')
# #lidar.connect(port="COM4", baudrate=115200, timeout=3)
# # Linux   : "/dev/ttyUSB0"
# # MacOS   : "/dev/cu.SLAB_USBtoUART"
# # Windows : "COM5"



# # info = lidar.get_info()
# # print(info)

# health = (lidar.get_health())[0]
# print(health)

# #Should print angle and distance
# count = lidar.iter_scans()


# for i, data in enumerate(count): 
#   data[:1]
#   for j, variables in enumerate(data):
#     print(variables[1], variables[2])
#   if i > 1:
#       print(i, len(data))
#       break



# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()

# print(len(list))
# print(list)
# 
# ---------------rpLiDAR_A2M4_R4 implementation-------------------------------
from mcs.firmware.rpLiDAR_A2M4_R4 import rpLiDAR_A2M4_R4

def run(globals):
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.Lidar_debug

    ## Boolean to indicate if the lidar should run.
    enabled = tFlags.Lidar_enabled

    ## The real angle due to frame.
    realRobotAngle = 17

    ## String used for debugging
    debugPrefix = "[LiDAR]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init Lidar controller")
    if enabled:
    # start lidar
        Lidar = rpLiDAR_A2M4_R4(tFlags.rpLiDAR_A2M4_R4_debug, tFlags.rpLiDAR_A2M4_R4_enabled, globals)
        status = Lidar.startup()
        if debug:
            print(status)

    # Main loop controlling the drive system.
    while globals['state'] != 'shutdown':
        
        if enabled:
            
            try:
                # 90 FOV, 85 inches
                angle = Lidar.clearance(90, 2159)
                
                if (angle >= 315):
                    globals['pivot'] = 'cw'
                    angle = (360 - angle) + realRobotAngle

                elif (angle >= 0 and angle <= 45):
                    globals['pivot'] = 'ccw'
                    angle = angle + realRobotAngle

                globals['degrees'] = angle
                
                if debug:
                    print(debugPrefix + f"Rotating {angle} " + globals['pivot'])

                # Wait until the pivot is done.
                while globals['driveState'] != 'completed':
                    time.sleep(2)

            except (KeyboardInterrupt,SystemExit):
                Lidar.stop_lidar()

    if enabled:
        Lidar.stop_lidar()
    if debug:
        print(debugPrefix + "Shutting down lidar")

