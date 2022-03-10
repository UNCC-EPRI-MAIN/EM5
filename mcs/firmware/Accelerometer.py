## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file Accelerometer.py
# Controls the wheel and blade motor relays.

import board
import adafruit_lis331

## This class is used to control individual normally open relays.
# If the relay is enabled, a simple digital out is sent triggering a MOSFET controlled relay.
class Accelerometer:

    ##  Constructor for accelerometer module. 
    # Relays are normally open and disabled by default
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out. If false, relays will always be open.
    def __init__(self, debugFlag, enabledFlag):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag

        ## Boolean to indicate if the accelermeter should be used.
        self.enabled = enabledFlag

        ## String for debugging
        self.debugPrefix = "[Accelerometer]"

        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"

        self.i2c = board.I2C()
        self.lis = adafruit_lis331.LIS331HH(self.i2c)

        if self.debug:
            print(self.debugPrefix + "[__init__()]: Using I2C Pins.")
            print(self.debugPrefix + "[__init__()]: Completed Setup of the accelerometer.")



    ## Closes relay by outputting high GPIO signal
    def GetReading(self):
        return self.lis.accleration