## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file BatteryMonitor.py
# Tells the robot when the battery is low or charged.

import RPi.GPIO as GPIO
import importlib

import mcs.PinAssignments as pins

## The function that the spawned process uses.
def run(globals):

    # load test flags
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.BatteryMonitor_debug

    ## Boolean to indicate if blade motors should be used. 
    enabled = tFlags.BatteryMonitor_enabled

    ## String used for debugging
    debugPrefix = "[Battery Monitor]"
    if enabled:
        debugPrefix += "[E]: "
    else:
        debugPrefix += "[D]: "  
    if debug:
        print(debugPrefix + "init battery monitor")
    if enabled:
        GPIO.setup(pins.ChargedBattery, GPIO.IN)
        GPIO.setup(pins.LowBattery, GPIO.IN)
    

    while globals['state'] != 'shutdown':

        if enabled:
            if GPIO.input(pins.LowBattery):
                globals['state'] = 'lowbattery'

            if GPIO.input(pins.ChargedBattery):
                globals['state'] = 'chargedbattery'
        

