## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file AMT103.py
# Reads the encoders on the wheels.
# This helps us with keeping the wheel straight and turning.

from distutils.log import debug
import RPi.GPIO as GPIO

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
            self.currentState = GPIO.input(self.pinXNumber)
            if self.debug:
                print(self.debugPrefix + "[__init__()]: Channel X BCM pin = " + str(pinXNumber))
        else:
            if self.debug:
                print(self.debugPrefix + "[__init__()]: Encoder is disabled.")

    
    ## Counts the pulses in a loop
    def run(self, globals):
        while globals['state'] != 'shutdown':
            if self.enabled:
                newState = GPIO.input(self.pinXNumber)
                if newState != self.currentState:

                    if self.debug:
                        print(self.debugPrefix + f"[run()]: Encoder Count: {self.count}")

                    self.count += 1
                    self.currentState = newState

    ## Return the encoder counter.
    def GetCount(self):
        return self.count

    ## Reset the counter.
    def ResetCount(self):
        self.count = 0
                    
                    
