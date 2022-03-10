## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file DriveControl.py
# Controls the wheel motors and implements driving and turning.

# standard libraries
import time
import RPi.GPIO as GPIO

import threading
import importlib

# module parameters
PIVOT_SPEED = 30
DISTANCE_WHEEL_TO_WHEEL = 93                            # distance in cm measured from center of wheel to other
PIVOT_CIRCUMFERENCE = 3.14 * DISTANCE_WHEEL_TO_WHEEL    # 292.02 cm
DISTANCE_PER_DEGREE = PIVOT_CIRCUMFERENCE / 360         # 0.811 cm for each degree
NORMAL_DRIVE_SPEED = 50
COURSE_CORRECTION_FACTOR = 0.2                          # higher number -> faster correction

# Load Initial Modules
import mcs.PinAssignments as pins

# Firmware modules
import mcs.firmware.RelayControl as RelayControl
import mcs.firmware.Sabertooth2x60 as Sabertooth2x60
import mcs.firmware.AMT103 as AMT103


## This class is the firmware used to control the wheel motors via the Sabertooth2x60 hardware.
# A PWM signal is passed throug the low pass filter, converting it to an analog signal. The Sabertooth2x60
# then uses the signal to control a motor. This class controls only a single motor via one PWM signal.
class DriveControl:

    ##  Constructor for motor module. 
    # Motor is initalized with a speed of zero. 
    # @param pinNumber Raspberry Pi GPIO board pin number used for PWM to drive single motor
    # @param flags System flags passed to module. Should be defined in test bench or SystemFlags module.
    # @param debugName Name of instance to be used for debugging output
    def __init__(self):
        
        flagpath = globals['flagFile']
        tFlags = importlib.import_module(flagpath)

        ## Boolean indicating if debug info should be included for this module
        self.debug = tFlags.DriveControl_debug

        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
        self.enabled = tFlags.DriveControl_enabled

        ## String used for debugging
        self.debugPrefix = "[DriveControl]"
        ## The speed of the left wheel.
        self.leftSpeed = 0
        ## The speed of the right wheel.
        self.rightSpeed = 0
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"  
        
        if self.debug:
            print(self.debugPrefix + "[__init__()]: defining DriveControl")
        if self.enabled:
            ## The relay class object.
            self.relay = RelayControl.RelayControl(pins.wheelRelay, tFlags.wheelRelay_debug, tFlags.wheelRelay_enabled, "Wheel")
            ## The left motor object.
            self.leftMotor = Sabertooth2x60.Sabertooth2x60(pins.leftMotorPWM, tFlags.leftMotor_debug, tFlags.leftMotor_enabled, "Left")
            ## The right motor object.
            self.rightMotor = Sabertooth2x60.Sabertooth2x60(pins.rightMotorPWM, tFlags.rightMotor_debug, tFlags.rightMotor_enabled, "Right")
            ## The left encoder object.
            self.leftEncoder = AMT103.AMT103(pins.leftEncoderX, pins.leftEncoderA, tFlags.leftEncoder_debug, tFlags.leftEncoder_enabled, "Left")
            ## The right encoder object.
            self.rightEncoder = AMT103.AMT103(pins.rightEncoderX, pins.rightEncoderA, tFlags.rightEncoder_debug, tFlags.rightEncoder_enabled, "Right")

    ## Makes the robot drive straight.
    # Does not use the encoder to move.
    def straight(self, speed):
        self.leftSpeed = speed
        self.rightSpeed = speed
        if self.debug:
            print(self.debugPrefix + "[stright()]: driving straight")
        if self.enabled:
            self.leftMotor.engage(speed)
            self.rightMotor.engage(speed)

    ## Makes the robot to move slightly left.
    # weird function. It doesnt use the degrees.
    def veerRightDegrees(self, degrees):
        if degrees > 90 or degrees <= 0:
            print("!--- Invalid degrees in veer right ---!")
        #self.leftSpeed = int(COURSE_CORRECTION_FACTOR * NORMAL_DRIVE_SPEED)
        #self.rightSpeed = NORMAL_DRIVE_SPEED
        self.leftSpeed = NORMAL_DRIVE_SPEED + 10
        self.rightSpeed = NORMAL_DRIVE_SPEED
        if self.debug:
            print(self.debugPrefix + "[veerRight()]: ")
        if self.enabled:
            self.leftMotor.engage(self.leftSpeed)
            self.rightMotor.engage(self.rightSpeed)

    ## Makes the robot to move slightly left.
    # weird function. It doesnt use the degrees.
    def veerLeftDegrees(self, degrees):
        if degrees > 90 or degrees <= 0:
            print("!--- Invalid degrees in veer left ---!")
        #self.leftSpeed = NORMAL_DRIVE_SPEED
        #self.rightSpeed = int(COURSE_CORRECTION_FACTOR * NORMAL_DRIVE_SPEED)
        self.leftSpeed = NORMAL_DRIVE_SPEED
        self.rightSpeed = NORMAL_DRIVE_SPEED + 10
        if self.debug:
            print(self.debugPrefix + "[veerLeft()]: ")
        if self.enabled:
            self.leftMotor.engage(self.leftSpeed)
            self.rightMotor.engage(self.rightSpeed)

    ## Turn the robot CW
    def pivotRight(self, degrees):
        distance  = int(degrees * DISTANCE_PER_DEGREE)
        if self.debug:
            print(self.debugPrefix + "[pivotRight()]: degrees = " + str(degrees))
            print(self.debugPrefix + "[pivotRight()]: distance (cm) to travel = " + str(distance))
        if self.enabled:
            thread_leftEncoder = threading.Thread(target = self.leftEncoder.countDown, args = (distance, ))
            thread_leftEncoder.start()
            self.leftMotor.engage(PIVOT_SPEED)
            self.rightMotor.engage(-PIVOT_SPEED)
            thread_leftEncoder.join()
            self.leftMotor.stop()
            self.rightMotor.stop()
            if self.debug:
                print(self.debugPrefix + "[pivotRight()]: pivot complete")

    ## Turn the robot CCW
    def pivotLeft(self, degrees):
        distance  = int(degrees * DISTANCE_PER_DEGREE)
        if self.debug:
            print(self.debugPrefix + "[pivotLeft()]: degrees = " + str(degrees))
            print(self.debugPrefix + "[pivotLeft()]: distance (cm) to travel = " + str(distance))
        if self.enabled:
            thread_leftEncoder = threading.Thread(target = self.leftEncoder.countDown, args = (distance, ))
            thread_leftEncoder.start()
            self.leftMotor.engage(-PIVOT_SPEED)
            self.rightMotor.engage(PIVOT_SPEED)
            thread_leftEncoder.join()
            self.leftMotor.stop()
            self.rightMotor.stop()
            if self.debug:
                print(self.debugPrefix + "[pivotLeft()]: pivot complete")


    ## Set the left motor speed.
    def manualSetLeftSpeed(self, speed):
        self.leftSpeed = speed
        if self.enabled:
                self.leftMotor.engage(speed)
            
    ## Set the speed to both motors.
    def setManualSpeed(self, newLeftSpeed, newRightSpeed):
        self.leftSpeed = newLeftSpeed
        self.rightSpeed = newRightSpeed
        if self.enabled:
            self.leftMotor.engage(newLeftSpeed)
            self.rightMotor.engage(newRightSpeed)

    ## Set the right motor speed.
    def manualSetRightSpeed(self, speed):
        self.rightSpeed = speed
        if self.enabled:
            self.rightMotor.engage(speed)
    
    ## Give power to the wheel motors.
    def enable(self):
        if self.debug:
            print(self.debugPrefix + "[enable()]: driving straight")
        if self.enabled:
            self.relay.enable()
    
    ## Disable the motors from receiving power.
    def disable(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[disable()]: driving straight")
        if self.enabled:
            self.relay.disable()

    ## Stops both wheel motors.
    def rapidStop(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[rapidStop()]: turning on motors")
        if self.enabled:
            self.leftMotor.stop()
            self.rightMotor.stop()
            self.relay.disable()

    ## Stops motor gently
    def stop(self):
        if self.debug:
            print(self.debugPrefix + "[stop()]: turning on motors")
        if self.enabled:
            self.speed = self.rightSpeed
            while self.speed > 0:
                self.speed -= 1
                self.leftMotor.engage(self.speed)
                self.rightMotor.engage(self.speed)
                time.sleep(0.01)
            
            self.speed = 0
            self.leftMotor.engage(self.speed)
            self.rightMotor.engage(self.speed)
            self.relay.disable()