## @package mcs.firmware.Bumper

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

## This class is used to control individual normally open bumper.
# @author Ithamar
# @note 02/28/2021: Created
class Bumper:

    ##  Constructor for bumper module. 
    # Relays are normally open and disabled by default 
    # @param pinNumber Interger Raspberry Pi GPIO BCM pin number used for control signal
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if operations should be carried out. If false, bumper will always be open.
    # @param debugName String to indicate name for debugging information
    def __init__(self, pinNumber, debugFlag, enabledFlag, overrideFlag, debugName):
        ## Boolean indicating if the program need to output debugging info.
        self.debug = debugFlag
        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors
        self.enabled = enabledFlag
        ## String to differentiate different bumper for debugging
        self.debugPrefix = "[Bumper<" + debugName + ">]"
        if overrideFlag:
            self.debugPrefix += "[O]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"
        self.pinNumber = pinNumber
        if self.enabled:
            GPIO.setup(pinNumber, GPIO.IN)
        if self.debug:
            print(self.debugPrefix + "[__init__()]: BCM pin = " + str(pinNumber))


    ## Open bumper by outputtting low digital output to relay's MOSFET
    def state(self):
        if self.enabled:
            state = GPIO.input(self.pinNumber)
        else:
            state = -1
        if self.debug:
            print(self.debugPrefix + "[state()]: pin status " + str(state))
        return state