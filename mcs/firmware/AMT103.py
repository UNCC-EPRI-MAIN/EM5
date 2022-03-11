## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file AMT103.py
# Reads the encoders on the wheels.
# This helps us with keeping the wheel straight and turning.

import RPi.GPIO as GPIO

# Module Parameters
GEAR_RATIO = 26                                                             # 26 motor rotations for one wheel rotation
INDEX_PULSE_PER_WHEEL_ROTATION = GEAR_RATIO                                 # index will pulse 26 times per wheel rotation
INDEX_CHANGE_PER_WHEEL_ROTATION = 2 * GEAR_RATIO                            # 26 pulses = 52 state changes on pin
WHEEL_DIAMETER = 33                                                         # diameter in cm
WHEEL_CIRCUMFERENCE = 3.14 * WHEEL_DIAMETER                                 # circumference in cm
DISTANCE_PER_STEP = WHEEL_CIRCUMFERENCE / INDEX_CHANGE_PER_WHEEL_ROTATION   # distance in cm for each step
DISTANCE_PER_STEP = 2                                                       # above calculation yields 1.99

## This class is the firmware read the encoders on the wheels.
class AMT103:

    ##  Constructor for relay control module. 
    # @param pinXNumber Interger Raspberry Pi GPIO BCM pin number used channel X of encoder
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out.
    # @param debugName String to indicate name for debugging information 
    def __init__(self, pinXNumber, debugFlag, enabledFlag, debugName):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag

        ## Boolean to indicate if this device should be used
        self.enabled = enabledFlag

        ## the encoder count 
        self.count = 0

        ## String to differentiate different relays for debugging
        self.debugPrefix = "[AMT103<" + debugName + ">]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"
        self.pinXNumber = pinXNumber

        if self.enabled:
            GPIO.setup(pinXNumber, GPIO.IN)
        if self.debug:
            print(self.debugPrefix + "[__init__()]: Channel X BCM pin = " + str(pinXNumber))

        self.currentState = GPIO.input(self.pinXNumber)

    ## Counts the pulses in a loop
    def run(self):
        while globals['state1'] != 'shutdown':
            if self.enabled:
                newState = GPIO.input(self.pinXNumber)
                if newState != self.currentState:
                    stepCount += 1
                    self.currentState = newState


    ## Return the encoder counter.
    def GetCount(self):
        return self.count
                    
                    
