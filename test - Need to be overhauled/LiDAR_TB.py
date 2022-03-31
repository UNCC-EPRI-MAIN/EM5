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

lidar = RPLidar('COM4')
#lidar.connect(port="COM4", baudrate=115200, timeout=3)
# Linux   : "/dev/ttyUSB0"
# MacOS   : "/dev/cu.SLAB_USBtoUART"
# Windows : "COM5"



# info = lidar.get_info()
# print(info)

health = lidar.get_health()
print(health)

# Should print angle and distance
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
#from mcs.firmware.rpLiDAR_A2M4_R4 import rpLiDAR_A2M4_R4 

#Globals
globals = dict()
#Super States
globals['state1'] = 'startup'

#Object Detection
globals['forwardClearance'] = 200
globals['leftTurnClear'] = False
globals['rightTurnClear'] = False
globals['avoidanceTurnDirection'] = None

start_angle = 0
end_angle = 45
distance_minimum = 304
#Function testing 
# LD = rpLiDAR_A2M4_R4(True, True)
# LD.startup()
count = lidar.iter_scans()
# # print(globals)
# LD.objectDetection(globals)
while globals['state1'] != 'shutdown':
  try:
    for i, data in enumerate(count): 
      data[:1]
      for j, variables in enumerate(data):
          # print(variables[2])
          if (330 < variables[1] < 360 ) or (0 < variables[1] < 60):
            if variables[2] < 200:
              print("Distance:", variables[2], "Angle:",variables[1])
            else:
              lidar.clean_input()


        # print(f"Angle: {variables[1]} Distance: {variables[2]}")

  except KeyboardInterrupt:
    print('Lidar Stoped')
    lidar.stop()
    lidar.stop_motor()
    lidar.clean_input()

lidar.disconnect()