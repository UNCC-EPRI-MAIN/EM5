## @package mcs.firmware
# The lowest level of the mcs responsible for controling each components.

## @file MD30C.py
# Drives the driver board for the blade motors.

import RPi.GPIO as GPIO

## This class is the firmware used to control the blade motor driver.
# A PWM signal is sent to the MD30C to indicate speed of blade motors.
# One signal is used for all three blade motors.
# Note: Blades will not spin if power is cut off by an open relay
# Blades are to be contolled by higher module -> BladeControl
class MD30C:

    ##  Constructor for blade motor module. 
    # Motor is initalized with a speed of zero. 
    # @param pinNumber Interger Raspberry Pi GPIO BCM pin number used for PWM to drive all 3 motors
    # @param debugFlag Boolean to indicate if debugging data should be printed
    # @param enabledFlag Boolean to indicate if opeations should be carried out
    def __init__(self, pinNumber, debugFlag, enabledFlag):
        ## Boolean indicating if debug info should be included for this module
        self.debug = debugFlag

        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors
        self.enabled = enabledFlag

        ## String used for debugging
        self.debugPrefix = "[MD30C]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"
        
        ## Dutycycle used for PWM signal. Initally set to 0 (motors stopped)
        self.dutyCycle = 0
        self.pinNumber = pinNumber
        if self.enabled:
            GPIO.setup(self.pinNumber, GPIO.OUT)
            ## PWM controller
            self.motorPWM = GPIO.PWM(self.pinNumber, 10000)
            self.motorPWM.start(self.dutyCycle)
        if self.debug:
            print(self.debugPrefix + "[__init__()]: BCM pin = " + str(self.pinNumber))

    ## Stops motor by setting PWM to 0
    def stop(self):
        self.dutyCycle = 0
        if self.enabled:
            self.motorPWM.ChangeDutyCycle(self.dutyCycle)
        if self.debug:
            print(self.debugPrefix + "[stop()]: speed = 0")
            print(self.debugPrefix + "[stop()]: PWM duty cycle = " + str(self.dutyCycle))

    ## Spins motors by setting PWM to 100
    def spin(self):
        self.dutyCycle = 25
        if self.enabled:
            self.motorPWM.ChangeDutyCycle(self.dutyCycle)
        if self.debug:
            print(self.debugPrefix + "[spin()]: PWM duty cycle = " + str(self.dutyCycle))