## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file Sabertooth2x60.py
# Controls the wheel motors.
# This interfaces with the sabertooth2x60 driver board.

import RPi.GPIO as GPIO

## This class is the firmware used to control the wheel motors via the Sabertooth2x60 hardware.
class Sabertooth2x60:

    ## Constructor for motor module. 
    # Motor is initalized with a speed of zero. 
    # @param pinNumber Interger Raspberry Pi GPIO BCM pin number used for PWM to drive single motor
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out
    # @param debugName String to indicate name for debugging information
    def __init__(self, pinNumber, debugFlag, enabledFlag, debugName):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag
        dutyCycle = 50

        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors
        self.enabled = enabledFlag

        ## String used for debugging
        self.debugPrefix = "[Sabertooth2x60<" + debugName + ">]"

        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"

        ## Dutycycle used for PWM signal. Initally set to 50 (motors stopped)
        ## Raspberry Pi GPIO BCM pin number for PWM output
        self.pinNumber = pinNumber
        if self.enabled:
            GPIO.setup(pinNumber, GPIO.OUT)
            
            ## PWM controller
            self.motorPWM = GPIO.PWM(pinNumber, 207)
            self.motorPWM.start(dutyCycle)

        if self.debug:
            print(self.debugPrefix + "[__init__()]: BCM pin = " + str(self.pinNumber))

    ## Stops motor by setting PWM to 50
    def stop(self):
        dutyCycle = 50
        if self.enabled:
            self.motorPWM.ChangeDutyCycle(dutyCycle)
        if self.debug:
            print(self.debugPrefix + "[stop()]: speed = 0")
            print(self.debugPrefix + "[stop()]: PWM duty cycle = " + str(dutyCycle))

    ## Engage motor forward using provided speed.
    # @param speed Speed should be greater than zero or less than or equal to 100 
    def engage(self, speed):

        # ensure speed is integer
        speed = int(speed)

        # ensure value isn't past max
        if speed > 100:
            speed = 100

        # isn't value above maximum reverse
        if speed < -100:
            speed = -100

        # stop
        if speed == 0:
            dutyCycle = 50

        # forward
        elif speed > 0:
            dutyCycle = int(speed / 100 * 50 + 50)

        # backwards
        else:
            dutyCycle = int(speed / 100 * 50 + 50)

        # Clamp valid duty cycles
        if dutyCycle > 100:
            dutyCycle = 100

        if dutyCycle < 0:
            dutyCycle = 0

        if self.enabled:
            self.motorPWM.ChangeDutyCycle(dutyCycle)
        if self.debug:
            print(self.debugPrefix + "[engage()]: speed = " + str(speed))
            print(self.debugPrefix + "[engage()]: PWM duty cycle = " + str(dutyCycle))