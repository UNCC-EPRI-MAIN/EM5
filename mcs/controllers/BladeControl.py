## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file BladeControl.py
# Provides high level control by integrating MD30C and relay control

# Standard libraries
import RPi.GPIO as GPIO
import importlib
GPIO.setmode(GPIO.BOARD)

# Load Initial Modules
import mcs.PinAssignments as pins

# Firmware modules
from mcs.firmware.RelayControl import RelayControl
from mcs.firmware.MD30C import MD30C

## The function that the spawned process uses.
def run(globals):

    # load test flags
    tFlags = importlib.import_module(globals['flagFile'])

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.BladeControl_debug

    ## Boolean to indicate if blade motors should be used. 
    enabled = tFlags.BladeControl_enabled

    ## Boolean to indicate if blade motors are on. 
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
        ## The relay class object. 
        relay = RelayControl(pins.bladeRelay, tFlags.bladeRelay_debug, tFlags.bladeRelay_enabled, "Blade")
        ## The Blade class object. 
        blade = MD30C(pins.bladePWM, tFlags.MD30C_debug, tFlags.MD30C_enabled)

    # main loop, run until end of program
    while globals['state1'] != 'shutdown':

        # check if change in state
        if globals['bladesOn'] != bladesOn:
            bladesOn = globals['bladesOn']
            
            # Turn off blades
            if not bladesOn:
                if debug:
                    print(debugPrefix + "turning off blades")
                if enabled:
                    blade.stop()
                    relay.disable()
            
            # Turn on blades
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


