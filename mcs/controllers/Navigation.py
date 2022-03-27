## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file Navigation.py
# Handle the GPS modules and keeps the robot on path.

# NOTE: Using RTK is the best method right now for us, but that requires a base station and one of the boards is not working.
# We are now stuck with 1.5m +- accuracy 
# Maybe later on, mapping with lidar with a GPS boundary would be the better method.

# standard libraries
import importlib
import threading

# Helper libraries
import math
import time
from geopy.distance import great_circle

# Firmware modules
import mcs.firmware.NEO_M9N as NEO_M9N
import mcs.firmware.Path as path

## The function that the spawned process uses.
def run(globals):

    # load test flags
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.Navigation_debug

    ## Boolean to indicate if the module is active. 
    enabled = tFlags.Navigation_enabled

    RATIO = 85 / 100

    ## Distance from the destination when we can take next waypoint.
    DISTANCE_THRESHOLD = 20

    ## The max amount of time the robot can be off course when GPS is scanned
    OFFCOURSE_MAX_COUNT = 5

    ## Running count of the amount of time the robot is off course when scanned.
    offcourse_count = 0

    ## The number degrees off the path before a pivot is needed.
    DEGREES_FORCE_PIVOT = 5                                                   

    mowbot_path = path.Path()

    currentDestination = None

    ## String used for debugging
    debugPrefix = "[Navigation]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init navigation controller")

    if enabled:
        # start GPS thread
        thread_gps = threading.Thread(target = NEO_M9N.run, args = (tFlags.NEO_M8P_debug, tFlags.NEO_M8P_enabled, globals))
        thread_gps.start()

    mowbot_path.LoadPathFromFile()

    # main loop, run until end of program
    while globals['state'] != 'shutdown':
        time.sleep(1)
        currentLon = globals['lon']
        currentLat = globals['lat']
        currentHeading = globals['heading']

        if globals['state'] == 'lowbattery':
           if not mowbot_path.RTB():
                currentDestination = mowbot_path.BackTrack()

        currentDestination = mowbot_path.GetCurrentWaypoint()
        destinationLat = currentDestination.lat
        destinationLon = currentDestination.long

        if debug:
            print(debugPrefix + f"Current Lat: {currentLat}, Current Lon: {currentLon}")
            print(debugPrefix + f"Destination Lat: {destinationLat}, Destination Lon: {destinationLon}")

        # make sure gps readings are good
        if currentLon != -1 and currentLat != -1:
            # get heading in radians
            # I dont know if is the right way to do this.
            destinationHeading = math.atan2(destinationLat - currentLat, RATIO * (destinationLon - currentLon))

            # convert to degreees and adjust for compass orienation
            # I dont know if is the right way to do this.
            destinationHeading = 90 - math.degrees(destinationHeading)

            # fix if less than zero
            if destinationHeading < 0:
                destinationHeading += 360

            if debug:
                print(debugPrefix + f"Destination Heading Angle: {destinationHeading}")

            if (destinationHeading - currentHeading) > DEGREES_FORCE_PIVOT:
                if offcourse_count < OFFCOURSE_MAX_COUNT:
                    
                    offcourse_count += 1
                    if debug:
                        print(debugPrefix + f"WARNING: the robot is off course.")

                else:
                    offcourse_count = 0
                    globals['degrees'] = (destinationHeading - currentHeading)
                    globals['pivot'] = 'cw'
                    globals['offcourse'] = True
                    if debug:
                        print(debugPrefix + f"Performing a pivot.")

            else:
                offcourse_count = 0
                globals['offcourse'] = False

            
            # Compute the distance from each other.
            p1 = (currentLat, currentLon)
            p2 = (destinationLat, destinationLon)
            distance = great_circle(p1, p2).meters

            if debug:
                print(debugPrefix + f": Distance from destination {distance}")

            # arrived at destination
            if distance < DISTANCE_THRESHOLD:
                
                if debug:
                    print(debugPrefix + f": Arrived at {currentDestination}")
                    print(debugPrefix + f": Getting next waypoint.")

                currentDestination = mowbot_path.NextWaypoint()

                # Done with the path.
                if currentDestination == None:
                    
                    if not mowbot_path.IsRTB():
                        if debug:
                            print(debugPrefix + ": No more path, returning to base")
                        
                        mowbot_path.BackTrack()
                    
                    else:
                        if debug:
                            print(debugPrefix + ": Back at base. Shutting down.")

                        globals['state'] = 'shutdown'
   

    # wait for threads to end
    if enabled:
        thread_gps.join()

    print(debugPrefix + "end of module")