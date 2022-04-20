# LiDAR Functions for obstacle detection, docking procedure and object tracking
# @author: Rene


from ast import Global
from turtle import left
from rplidar import RPLidar as LD
from math import floor, cos, sin, pi



class rpLiDAR_A2M4_R4:

    ##  Constructor for GNSS module 
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out
    def __init__(self, debugFlag, enabledFlag, globals):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag
        ## Boolean to indicate if the LiDAR should be used. If disabled, program will run but return -1 for all values.
        self.enabled = enabledFlag
        ## String used for debugging
        self.debugPrefix = "[rpLiDAR_A2M4_R4]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"
        if self.enabled:
            #Lunix
            self.lidar = LD('/dev/ttyUSB0')
            #Windows
            #self.lidar = LD('COM9')
        if self.debug:
            print(self.debugPrefix + "[__init__()]: LiDAR Initialized]")
    
    # Self check function, restarting LiDAR if not functioning properly
    def  startup(self):
         up_status = False
         status_string = ''
         health = self.lidar.get_health()
         while not up_status:
             self.lidar.connect()
#              self.lidar.start_motor()  # may not be needed as get_health starts motor i think
             if health[0] != 'Good':
                  self.lidar.stop()
                  self.lidar.stop_motor()
                  self.lidar.disconnect()
                  status_string = 'LiDAR Not Good - Restarting'
             elif health[0] == 'Good':
                  up_status = True
                  status_string = 'LiDAR up and Running - Proceed'
             return status_string
         
                  
   
   
    # Helper fuction to run the LiDAR during docking operations, calculating distance from the guide rails, returning distance and angle
    # def docking_guide_distance_helper(data):
    #     distance_to_middle = 31.115
    #     while True:
    #         distance_left_rail = data[314] * 0.1
    #         distance_right_rail = data[134] * 0.1
    #         if distance_left_rail > distance_to_middle:
    #             turn_left = True
    #         elif distance_right_rail > distance_to_middle:
    #             turn_right = True
    #         elif (distance_left_rail, distance_right_rail) == distance_to_middle:
    #             turn_left, turn_right = False
    #             go_straight = True
    def stop_lidar(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.clean_input()
        # self.lidar.disconnect()

    # Function to find the angle of closes object in a given Horizontal FOV
    def clearance(self, FOV, min_distance):
        count = self.lidar.iter_scans()
        left_angle = 360 - (FOV/2)
        right_angle = (FOV/2)
        for i, data in enumerate(count):

            if globals['state'] == 'shutdown':
                break

            data[:1]
            #variables[0] is scan quality, variables[1] is Angle, variables[2] is distance
            for j, variables in enumerate(data):
                #Left side of Robot
                if (left_angle < (variables)[1] < 360 ):
                    if variables[2] < min_distance:
                #   print("Distance:", variables[2], "Angle:",variables[1])
                        print('Pivit cw by:',variables[1])
                        return False
                #Right side of Robot
                elif (0 < variables[1] < right_angle):
                    if variables[2] < min_distance:
                        print('Pivit ccw by:',variables[1])
                        return False


            # print(f"Angle: {variables[1]} Distance: {variables[2]}")

    # helper function used to find objects/obstacles obstructing the robot path
    # distance variables are in mm/cm (data distance is initially in mm, but is changed to cm)
    # def lidar_object_helper(self, data):
    #     front_left_angle = 0
    #     front_right_angle = 90
    #     front_min_distance = 200            # 2 meters -- change to desired maximum front distance
    #     side_min_distance = 610             # distance in mm from the center of the robot to the sides (min distance needed for object to clear the robot)
    #     line_of_scrimmage = 50              # Distance in cm, from the LiDAR to the front edge of the robot
    #     front_angle = 45                    # the angle pointing directly to the front of the robot
    #     distance_right = 0                  # initialized object distance to the right of the front angle to 0
    #     distance_left = 0                   # initialized object distance to the left of the front angle to 0
    #     distance_front = front_min_distance # initialized the distance of an object to the front of the robot as the max viewing distance
        
    #     min_dist = front_min_distance               # Initializing the minimum distance seen by the lidar to the max value in the data, to compute actual min
    #     min_angle = 0
    #     for angle in range(front_left_angle, front_right_angle, 1):
            
    #         distance = data[angle]
    #         if distance != 0:
    #             if angle > front_angle:
    #                 distance_front_temp = cos(((angle-front_angle)* pi)/180)*distance
    #                 distance_right = sin(((angle-front_angle)* pi)/180)*distance
    #                 distance_left = 1
    #             elif angle < front_angle:
    #                 distance_front_temp = cos(((front_angle - angle)*pi)/180) * distance
    #                 distance_left = sin(((front_angle - angle)* pi)/180)*distance
    #                 distance_right = 1
    #             else:
    #                 distance_front_temp = distance
    #                 distance_left = 0
    #                 distance_right = 0
    #             distance_front_temp = distance_front_temp * 0.1 - line_of_scrimmage
    #             if distance_front_temp < min_dist and distance_front_temp > 0 and distance_left < side_min_distance and distance_right < side_min_distance:
    #                 distance_front = distance_front_temp
    #                 min_angle = angle
    #                 min_dist = min(min_dist, distance_front_temp)
    #     # print closest value
    #     #print("Distance to object : ", distance_front, "cm at ", min_angle)
    #     return int(distance_front)
    #     #globals['forwardClearance'] = int(distance_front)


    # Function to find objects obstructing the path of the robot and returning distance to the objects
    def objectDetection(self, globals):
        if self.enabled:
            while globals['state1'] != 'shutdown': 
                try:
                # process of getting LiDAR read outs each scan will call the function to analyze the data
                    for scan in self.lidar.iter_scans():
                        if globals['state1'] == 'shutdown':
                            break
                        scan_data = [0]*360
                        scan_data_mod = [0]*360
                        for (_, angle, distance) in scan:
                            scan_data[min([359, floor(angle)])] = distance
                            newAngle = floor(angle) + 45
                            if newAngle > 359:
                                newAngle = newAngle - 360
                            scan_data_mod[newAngle] = distance    
                        forwardClearance = self.lidar_object_helper(scan_data_mod)
                        globals['forwardClearance'] = forwardClearance
                        
                        # Future: add if to only run in object avoidance
                        left_clearance = self.clearance(315, 359, scan_data_mod, 100)
                        globals['leftTurnClear'] = left_clearance
                        #right_clearance = self.clearance(0, 90, scan_data_mod, 100)
                        #globals['rightTurnClear'] = right_clearance

                        if self.debug:
                            print(self.debugPrefix + "[objectDetection()]: front clearance = " + str(forwardClearance))

                except KeyboardInterrupt:
                    print('Lidar failed')            
                    self.lidar.stop()
                    self.lidar.stop_motor()
                    self.lidar.disconnect()

            if self.debug:
                print(self.debugPrefix + "[objectDetection()]: Clean LiDar shutdown")
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()

    # def lidar_docking():
    #     try:
    #     # process of getting LiDAR read outs each scan will call the function to analyze the data
    #         print(lidar.get_info)
    #         for scan in lidar.iter_scans():
    #             scan_data = [0]*360
    #             for (_, angle, distance) in scan:
    #                 scan_data[min([359, floor(angle)])] = distance
    #             #process_data(scan_data)
    #             docking_guide_distance_helper(scan_data)
    #     except KeyboardInterrupt:
    #         print('Stoping.')
    #         lidar.stop()
    #         lidar.stop_motor()
    #         lidar.disconnect()

