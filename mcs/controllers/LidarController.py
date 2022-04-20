# ----------------------RPLidar Functions----------------------
#$ pip install rplidar-roboticia


from cmath import exp
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
import mcs.Flags as tFlags

def run(globals):
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.Lidar_debug

    ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
    enabled = tFlags.Lidar_enabled

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
        Lidar = rpLiDAR_A2M4_R4(tFlags.rpLiDAR_A2M4_R4_debug, tFlags.rpLiDAR_A2M4_R4_enabled)

    # Main loop controlling the drive system.
    while globals['state'] != 'shutdown':
        
        if enabled:

            if debug:
                print(Lidar.startup())

            # 90 FOV, 85 inches
            clear = Lidar.clearance(90, 2159)
            try:
                while clear:
                    print(clear)

                print('Crash')
                Lidar.stop_lidar()
                globals['state'] = 'shutdown'
            except (KeyboardInterrupt,SystemExit):
                Lidar.stop_lidar()



