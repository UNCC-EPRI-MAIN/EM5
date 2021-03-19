# standard libraries
import RPi.GPIO as GPIO
import importlib
GPIO.setmode(GPIO.BCM) 
import mcs.pinAssignments as pins
from mcs.firmware.RelayControl import RelayControl
from mcs.firmware.MD30C import MD30C

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
    debug = tFlags.BladeControl_debug
    ## Boolean to indicate if blade motors should be used. 
    enabled = tFlags.BladeControl_enabled
    bladesOn = False
    ## String used for debugging
    debugPrefix = "[BladeControl]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init blade controller")
    if enabled:
        relay = RelayControl(pins.bladeRelay, tFlags.bladeRelay_debug, tFlags.bladeRelay_enabled, tFlags.RelayControl_over, "Blade")
        blade = MD30C(pins.bladePWM, tFlags.MD30C_debug, tFlags.MD30C_enabled)

    
    # main loop, run until end of program
    while globals['state1'] != 'shutdown':

        # check if change in state
        if globals['bladesOn'] != bladesOn:
            bladesOn = globals['bladesOn']
            
            # turn off blades
            if not bladesOn:
                if debug:
                    print(debugPrefix + "turning off blades")
                if enabled:
                    blade.stop()
                    relay.disable()
            
            # turn on blades
            else:
                if debug:
                    print(debugPrefix + "turning on blades")
                if enabled:
                    relay.enable()
                    blade.spin()
    if debug:
        print(debugPrefix + "turning off blades")
    if enabled:
        blade.stop()
        relay.disable()
    print(debugPrefix + "end of module")


