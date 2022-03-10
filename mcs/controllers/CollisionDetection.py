## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file CollisionDetection.py
# Provides high level control by integrating MD30C and relay control

# Load Initial Modules
import importlib
import mcs.PinAssignments as pins

# Firmware modules
# Accelometer will be here.

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
    if debug:
        print(debugPrefix + "[run()]: Collision Detection initialized")
    activeCollision = False
    if enabled:
        if debug:
            print(debugPrefix + ": This modules is missing collision stuff.")

    while globals['state1'] != 'shutdown':
        if enabled:
            print(debugPrefix + ": This modules is missing collision stuff.")
            
    print(debugPrefix + "end of module")
                