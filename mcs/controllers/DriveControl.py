## @package mcs.controllers
#  Documentation for this module.
#
#  More details.

# standard libraries
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 
import importlib
import threading

# module parameters
PIVOT_SPEED = 30
DISTANCE_WHEEL_TO_WHEEL = 93 # distance in cm measured from center of wheel to other
PIVOT_CIRCUMFERENCE = 3.14 * DISTANCE_WHEEL_TO_WHEEL # 292.02 cm
DISTANCE_PER_DEGREE = PIVOT_CIRCUMFERENCE / 360 # 0.811 cm for each degree
NORMAL_DRIVE_SPEED = 50
COURSE_CORRECTION_FACTOR = 0.2 # higher number -> faster correction

# mcs modules
import mcs.pinAssignments as pins
import mcs.testFlags as tFlags
# relay control module
if tFlags.RelayControl_over:
    testDir = "test.routines.test" + str(tFlags.testNum) + ".RelayControl"
    relay_control = importlib.import_module(testDir)
else:
    import mcs.firmware.RelayControl as RelayControl
# sabertooth module
if tFlags.Sabertooth2x60_over:
    testDir = "test.routines.test" + str(tFlags.testNum) + ".Sabertooth2x60"
    Sabertooth2x60 = importlib.import_module(testDir)
else:
    import mcs.firmware.Sabertooth2x60 as Sabertooth2x60

# encoders module
if tFlags.AMT103_over:
    testDir = "test.routines.test" + str(tFlags.testNum) + ".AMT103"
    AMT103 = importlib.import_module(testDir)
else:
    import mcs.firmware.AMT103 as AMT103

## This class is the firmware used to control the wheel motors via the Sabertooth2x60 hardware.
# A PWM signal is passed throug the low pass filter, converting it to an analog signal. The Sabertooth2x60
# then uses the signal to control a motor. This class controls only a single motor via one PWM signal.
# @author Keith
# @note 11/26/2020: Added commenting to code. -KS
# @note 11/01/2020: Module tested. -KS
class DriveControl:

    ##  Constructor for motor module. 
    # Motor is initalized with a speed of zero. 
    # @param pinNumber Raspberry Pi GPIO board pin number used for PWM to drive single motor
    # @param flags System flags passed to module. Should be defined in test bench or SystemFlags module.
    # @param debugName Name of instance to be used for debugging output
    def __init__(self):
        
        ## Boolean indicating if debug info should be included for this module
        self.debug = tFlags.DriveControl_debug
        ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
        self.enabled = tFlags.DriveControl_enabled
        ## String used for debugging
        self.debugPrefix = "[DriveControl]"
        self.leftSpeed = 0
        self.rightSpeed = 0
        if tFlags.DriveControl_over:
            self.debugPrefix += "[O]"
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"  
        if self.debug:
            print(self.debugPrefix + "[__init__()]: defining DriveControl")
        if self.enabled:
            self.relay = RelayControl.RelayControl(pins.wheelRelay, tFlags.wheelRelay_debug, tFlags.wheelRelay_enabled, tFlags.RelayControl_over, "Wheel")
            self.leftMotor = Sabertooth2x60.Sabertooth2x60(pins.leftMotorPWM, tFlags.leftMotor_debug, tFlags.leftMotor_enabled, tFlags.Sabertooth2x60_over, "Left")
            self.rightMotor = Sabertooth2x60.Sabertooth2x60(pins.rightMotorPWM, tFlags.rightMotor_debug, tFlags.rightMotor_enabled, tFlags.Sabertooth2x60_over, "Right")
            self.leftEncoder = AMT103.AMT103(pins.leftEncoderX, pins.leftEncoderA, tFlags.leftEncoder_debug, tFlags.leftEncoder_enabled, tFlags.AMT103_over, "Left")
            self.rightEncoder = AMT103.AMT103(pins.rightEncoderX, pins.rightEncoderA, tFlags.rightEncoder_debug, tFlags.rightEncoder_enabled, tFlags.AMT103_over, "Right")

    ## Stops motor by setting PWM to 50.
    def straight(self, speed):
        self.leftSpeed = speed
        self.rightSpeed = speed
        if self.debug:
            print(self.debugPrefix + "[stright()]: driving straight")
        if self.enabled:
            self.leftMotor.engage(speed)
            self.rightMotor.engage(speed)

    ## Stops motor by setting PWM to 50.
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

    ## Stops motor by setting PWM to 50.
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

    ## Stops motor by setting PWM to 50.
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

    ## Stops motor by setting PWM to 50.
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


    ## Stops motor by setting PWM to 50.
    def manualSetLeftSpeed(self, speed):
        self.leftSpeed = speed
        if self.enabled:
                self.leftMotor.engage(speed)
            
    ## Stops motor by setting PWM to 50.
    def setManualSpeed(self, newLeftSpeed, newRightSpeed):
        self.leftSpeed = newLeftSpeed
        self.rightSpeed = newRightSpeed
        if self.enabled:
            self.leftMotor.engage(newLeftSpeed)
            self.rightMotor.engage(newRightSpeed)

    ## Stops motor by setting PWM to 50.
    def manualSetRightSpeed(self, speed):
        self.rightSpeed = speed
        if self.enabled:
            self.rightMotor.engage(speed)
    
    ## Stops motor by setting PWM to 50.
    def enable(self):
        if self.debug:
            print(self.debugPrefix + "[enable()]: driving straight")
        if self.enabled:
            self.relay.enable()
    
    ## Stops motor by setting PWM to 50.
    def disable(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[disable()]: driving straight")
        if self.enabled:
            self.relay.disable()

    ## Stops motor by setting PWM to 50.
    def rapidStop(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[rapidStop()]: turning on motors")
        if self.enabled:
            self.leftMotor.stop()
            self.rightMotor.stop()
            self.relay.disable()

    ## Stops motor by setting PWM to 50.
    def stop(self):
        if self.debug:
            print(self.debugPrefix + "[stop()]: turning on motors")
        if self.enabled:
            self.leftSpeed = self.rightSpeed
            while self.leftSpeed > 0:
                self.leftSpeed -= 1
                self.leftMotor.engage(self.leftSpeed)
                self.rightMotor.engage(self.rightSpeed)
                time.sleep(0.01)
            self.speed = 0
            self.leftMotor.engage(self.speed)
            self.rightMotor.engage(self.speed)
            self.relay.disable()