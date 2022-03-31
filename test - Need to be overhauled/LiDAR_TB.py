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
import mcs.testFlags as Flag
#Globals
# globals = dict()
# #Super States
# globals['state1'] = 'startup'
# #Object Detection
# globals['forwardClearance'] = 200
# globals['leftTurnClear'] = False
# globals['rightTurnClear'] = False
# globals['avoidanceTurnDirection'] = None

# start_angle = 0
# end_angle = 45
# FOV = 90
# min_distance = 200
# left_angle = 360 - (FOV/2)
# right_angle = (FOV/2)
# #Function testing 
# # LD = rpLiDAR_A2M4_R4(True, True)
# # LD.startup()
# count = lidar.iter_scans()
# # # # print(globals)
# # # LD.objectDetection(globals)
# while globals['state1'] != 'shutdown':
#   try:
#     for i, data in enumerate(count): 
#             data[:1]
#             #variables[0] is scan quality, variables[1] is Angle, variables[2] is distance
#             for j, variables in enumerate(data):
#                 if (left_angle < (variables)[1] < 360 ) or (0 < variables[1] < right_angle):
#                     if variables[2] < min_distance:
#                       print("Distance:", variables[2], "Angle:",variables[1])
#             else:
#               lidar.clean_input()


#         # print(f"Angle: {variables[1]} Distance: {variables[2]}")

#   except (KeyboardInterrupt,SystemExit):
#     print('Lidar Stoped')
#     lidar.stop()
#     lidar.stop_motor()
#     lidar.clean_input()
#     break
# lidar.disconnect()

Lidar = rpLiDAR_A2M4_R4(Flag.rpLiDAR_A2M4_R4_debug, Flag.rpLiDAR_A2M4_R4_enabled)

print(Lidar.startup())
clear = Lidar.clearance(90, 200)
try:
  while clear:
    print(clear)

  print('Crash')
  Lidar.stop_lidar()
except (KeyboardInterrupt,SystemExit):
  Lidar.stop_lidar()



