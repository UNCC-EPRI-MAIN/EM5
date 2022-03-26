## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file NEO_M8P.py
# Find the location of the Mowbot via gps

import serial
from ublox_gps import UbloxGps

# module parameters
FAILED_READ_ALARM_THRESHOLD = 3
FAILED_READ_ALARM_FREQUENCY = 10

def run(debug, enabled, globals):
    ## Used for debugging
    newLon = -1
    newLat = -1
    oldLon = -1
    oldLat = -1
    newHeading = -1
    oldHeading = -1

    debugPrefix = "[NEO_M9N]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"

    if enabled:
        try:
            port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
            gps = UbloxGps(port)
            failedReadCount = 0
            while globals['state'] != 'shutdown':
                try:
                    geo = gps.geo_coords()
                    newLon = geo.lon
                    newLat = geo.lat
                    newHeading = geo.headMot

                    if newLon != oldLon:
                        globals['lon'] = newLon
                        oldLon = newLon

                    if newLat != oldLat:
                        globals['lat'] = newLat
                        oldLat = newLat

                    if newHeading != oldHeading:
                        globals['heading'] = newHeading

                    if debug:
                        print(debugPrefix + "[run()]: X: " + str(geo.lon) + " Y: " + str(geo.lat))
                        print(debugPrefix + "[run()]: heading: " + str(geo.headMot))
                
                except (ValueError, IOError) as err:
                    failedReadCount += 1
                    if debug:
                        print(debugPrefix + err)
                        print(debugPrefix + "[run()]: failed read")
                    if failedReadCount >= FAILED_READ_ALARM_THRESHOLD and failedReadCount % 10 == 0:
                        print("!--- READ FAILURE ---!")
        except Exception as e:
            print("Failed to find the USB for the GPS.")
            print(e)
    
    print(debugPrefix + "end of module")