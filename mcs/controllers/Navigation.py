## @package mcs.controllers
#  Documentation for this module.
#
#  More details.

# standard libraries
import importlib
import threading
import multiprocessing as multiproc
from dataclasses import dataclass
import math
import time
from geopy.distance import great_circle
from vincenty import vincenty
#from geopy.distance import vincenty

import mcs.pinAssignments as pins

ratio = 85 / 100
DISTANCE_THRESHOLD = 4

@dataclass
class waypoint:
    lon: float
    lat: float

#A = waypoint(-80.7096746, 35.2376407)
B = waypoint(-80.7096318999, 35.2376935)
C = waypoint(-80.7096234999, 35.2376129999)
A = waypoint(-80.709662, 35.2376715)

## This class is the high level controller for the blade motors
# Provides high level control by integrating MD30C and relay control
# @author Keith
# @note 12/16/2020: Added commenting to code. -KS
def run(globals):

    # load test flags
    import mcs.testFlags as tFlags
    if tFlags.testNum > 0:
        testFile = "test.routines.test" + str(tFlags.testNum) + ".testFlags"
        tFlags = importlib.import_module(testFile)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.Navigation_debug
    ## Boolean to indicate if blade motors should be used. 
    enabled = tFlags.Navigation_enabled
    ## String used for debugging
    debugPrefix = "[Navigation]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init blade controller")

        
    if enabled:
        # load GPS module
        if tFlags.NEO_M8P_over:
            testDir = "test.routines.test" + str(testNum) + ".NEO_M8P"
            NEO_M8P = importlib.import_module(testDir)
        else:
            import mcs.firmware.NEO_M8P as NEO_M8P
        # start GPS thread
        thread_gps = threading.Thread(target = NEO_M8P.run, args = (tFlags.NEO_M8P_debug, tFlags.NEO_M8P_enabled, tFlags.NEO_M8P_RTK_enabled, tFlags.NEO_M8P_over, pins.rtkStatus, globals))
        thread_gps.start()

    # main loop, run until end of program
    if enabled:
        
        # go to waypoint A
        destinationLon = A.lon
        destinationLat = A.lat
        arrivedA = False
        arrivedB = False
        arrivedC = False

        while globals['state1'] != 'shutdown':
            time.sleep(1)
            currentLon = globals['lon']
            currentLat = globals['lat']
            # make sure gps readings are good
            if currentLon != -1 and currentLat != -1:
                # get heading in radians
                destinationHeading = math.atan2(destinationLat - currentLat, ratio * (destinationLon - currentLon))
                # convert to degreees and adjust for compass orienation
                destinationHeading = 90 - math.degrees(destinationHeading)
                # fix if less than zero
                if destinationHeading < 0:
                    destinationHeading += 360
                #if debug:
                #    print(debugPrefix + ": destination heading = " + str(destinationHeading))
                globals['destinationHeading'] = destinationHeading
                p1 = (currentLat, currentLon)
                p2 = (destinationLat, destinationLon)
                distance = great_circle(p1, p2).meters
                #distance = vincenty(p1, p2) * 1000
                #print(str(distance))
                # arrived at destination
                if False:
                #if distance < DISTANCE_THRESHOLD:
                    print("destination reached ---")
                    print(str(distance))
                    if not arrivedA:
                        arrivedA = True
                        destinationLon = B.lon
                        destinationLat = B.lat
                        print("destination A reached")
                    elif not arrivedB:
                        arrivedB = True
                        destinationLon = C.lon
                        destinationLat = C.lat
                        print("destination B reached")
                    elif not arrivedC:
                        print("destination C reached")
                        globals['state1'] = 'shutdown'
                    else:
                        print("something went wrong")
    # wait for threads to end
    if enabled:
        thread_gps.join()

    print(debugPrefix + "end of module")