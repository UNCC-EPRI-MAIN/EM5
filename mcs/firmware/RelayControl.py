

# standard libraries
import RPi.GPIO as GPIO

## This class is used to control individual normally open relays.
# If the relay is enabled, a simple digital out is sent triggering a MOSFET controlled relay.
class RelayControl:

    ##  Constructor for relay control module. 
    # Relays are normally open and disabled by default 
    # @param pinNumber Interger Raspberry Pi GPIO BCM pin number used for control signal
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out. If false, relays will always be open.
    # @param debugName String to indicate name for debugging information
    # @param overrideFlag Boolean to indicate module has been overridden 
    def __init__(self, pinNumber, debugFlag, enabledFlag, overrideFlag, debugName):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag
        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors
        self.enabled = enabledFlag
        ## String to differentiate different relays for debugging
        self.debugPrefix = "[RelayControl<" + debugName + ">]"
        if overrideFlag:
            self.debugPrefix += "[O]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"
        self.pinNumber = pinNumber
        if self.enabled:
            GPIO.setup(pinNumber, GPIO.OUT)
            GPIO.output(self.pinNumber, GPIO.LOW)
        if self.debug:
            print(self.debugPrefix + "[__init__()]: BCM pin = " + str(pinNumber))

    ## Closes relay by outputting high GPIO signal
    def enable(self):
        if self.enabled:
            GPIO.output(self.pinNumber, GPIO.HIGH)
        if self.debug:
            print(self.debugPrefix + "[enable()] closing relay")

    ## Open's relay by outputting low GPIO signal
    def disable(self):
        if self.enabled:
            GPIO.output(self.pinNumber, GPIO.LOW)
        if self.debug:
            print(self.debugPrefix + "[disable()]: opening relay ")