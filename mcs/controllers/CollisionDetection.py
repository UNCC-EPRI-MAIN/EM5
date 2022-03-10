## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file CollisionDetection.py
# Detect Collision with the bumpers and accleometer.

# Load Initial Modules
import importlib
import mcs.PinAssignments as pins

# Firmware modules
import mcs.firmware.Accelerometer as accelerometer

# Module Parameters
## x-axis accleration threshold in m/s^2
X_THRESHOLD = 10                     

## y-axis accleration threshold in m/s^2
X_THRESHOLD = 10

## z-axis accleration threshold in m/s^2
X_THRESHOLD = 10

## The function that the spawned process uses.
def run(globals):
    
    # load test flags
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)
    
    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.CollisionDetection_debug

    ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
    enabled = tFlags.CollisionDetection_enabled

    ## String used for debugging
    debugPrefix = "[CollisionDetection]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"

    if enabled:
        acc = accelerometer.Accelerometer(pins.SDA, pins.SDL, tFlags.accelerometer_debug, tFlags.accelerometer_debug)

    if debug:
        print(debugPrefix + "[run()]: Collision Detection initialized")

    while globals['state1'] != 'shutdown':
        if enabled:
            x, y, z = acc.GetReading()

            if abs(x) > X_THRESHOLD:
                activeCollision = True

            if abs(x) > X_THRESHOLD:
                activeCollision = True

            if abs(x) > X_THRESHOLD:
                activeCollision = True

            if activeCollision:
                if debug:
                    print(debugPrefix + "[run()]: Collision Detected.")
                    print(debugPrefix + "[run()]: Sending Shutdown Signal.")
                globals['state1'] = 'shutdown'
            
    print(debugPrefix + "end of module")
                