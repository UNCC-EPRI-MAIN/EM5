

import serial
from ublox_gps import UbloxGps
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module parameters
FAILED_READ_ALARM_THRESHOLD = 3
FAILED_READ_ALARM_FREQUENCY = 10

def run(debug, enabled, rtk_enabled, overrideFlag, rtkStatusPin, globals):
    ## String used for debugging
    newLon = -1
    newLat = -1
    oldLon = -1
    oldLat = -1
    newHeading = -1
    oldHeading = -1
    debugPrefix = "[NEO_M8P]"
    if overrideFlag:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"
    if rtk_enabled:
        debugPrefix += "[RTK]"
    if enabled:
        port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
        gps = UbloxGps(port)
        GPIO.setup(rtkStatusPin, GPIO.IN)
        failedReadCount = 0
        while globals['state1'] != 'shutdown':
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
                if newHeading != oldHeading and not globals['headingLock']:
                    globals['heading'] = newHeading
                rtkStatus = GPIO.input(rtkStatusPin)
                rtkStatus = not rtkStatus
                if rtkStatus:
                    failedReadCount = 0
                if debug:
                    print(debugPrefix + "[run()]: RTK active = " + str(rtkStatus))
                    print(debugPrefix + "[run()]: X: " + str(geo.lon) + " Y: " + str(geo.lat))
                    print(debugPrefix + "[run()]: heading: " + str(geo.headMot))
            except:
                failedReadCount += 1
                if debug:
                    print(debugPrefix + "[run()]: failed read")
                if failedReadCount >= FAILED_READ_ALARM_THRESHOLD and failedReadCount % 10 == 0:
                    print("!--- RTK READ FAILURE ---!")
    
    print(debugPrefix + "end of module")