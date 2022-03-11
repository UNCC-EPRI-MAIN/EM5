## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file DriveControl.py
# Controls the wheel motors and implements driving and turning.

# standard libraries
import time

import threading
import importlib

# module parameters
PIVOT_SPEED = 30
DISTANCE_WHEEL_TO_WHEEL = 93                            # distance in cm measured from center of wheel to other
PIVOT_CIRCUMFERENCE = 3.14 * DISTANCE_WHEEL_TO_WHEEL    # 292.02 cm
DISTANCE_PER_DEGREE = PIVOT_CIRCUMFERENCE / 360         # 0.811 cm for each degree
NORMAL_DRIVE_SPEED = 50
COURSE_CORRECTION_FACTOR = 0.2                          # higher number -> faster correction


GEAR_RATIO = 26                                                             # 26 motor rotations for one wheel rotation
INDEX_PULSE_PER_WHEEL_ROTATION = GEAR_RATIO                                 # index will pulse 26 times per wheel rotation
INDEX_CHANGE_PER_WHEEL_ROTATION = 2 * GEAR_RATIO                            # 26 pulses = 52 state changes on pin
WHEEL_DIAMETER = 33                                                         # diameter in cm
WHEEL_CIRCUMFERENCE = 3.14 * WHEEL_DIAMETER                                 # circumference in cm
DISTANCE_PER_STEP = WHEEL_CIRCUMFERENCE / INDEX_CHANGE_PER_WHEEL_ROTATION   # distance in cm for each step

# Module Parameters
NORMAL_DRIVE_SPEED = 50                     # Speed of the wheels normals
CAUTION_DRIVE_SPEED = 40                    # speed of the wheels when 
OBJECT_DETECTION_SLOW_DOWN_FACTOR = 1.5     # lower number -> more gradual slowdown
OBJECT_DETECTION_STOP_DISTANCE = 15         # cm
PIVOT_SPEED = 18                            # % motor speed
DEGREES_OFF_COURSE = 5                      # threshold to determine MowBot is off course
DEGREES_FORCE_PIVOT = 90                    # number of degrees off course requiring pivot

# Load Initial Modules
import mcs.PinAssignments as pins

# Firmware modules
import mcs.firmware.RelayControl as RelayControl
import mcs.firmware.Sabertooth2x60 as Sabertooth2x60
import mcs.firmware.AMT103 as AMT103

## The function that the spawned process uses.
def run(globals):
    flagpath = globals['flagFile']
    tFlags = importlib.import_module(flagpath)

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.DriveControl_debug

    ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
    enabled = tFlags.DriveControl_enabled

    ## String used for debugging
    debugPrefix = "[DriveControl]"
        
    ## The speed of the left wheel.
    leftSpeed = 0
    
    ## The speed of the right wheel.
    rightSpeed = 0
        
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"

    if enabled:
        ## The relay class object.
        relay = RelayControl.RelayControl(pins.wheelRelay, tFlags.wheelRelay_debug, tFlags.wheelRelay_enabled, "Wheel")
        ## The left motor object.
        leftMotor = Sabertooth2x60.Sabertooth2x60(pins.leftMotorPWM, tFlags.leftMotor_debug, tFlags.leftMotor_enabled, "Left")
        ## The right motor object.
        rightMotor = Sabertooth2x60.Sabertooth2x60(pins.rightMotorPWM, tFlags.rightMotor_debug, tFlags.rightMotor_enabled, "Right")
        
        ## The left encoder object.
        leftEncoder = AMT103.AMT103(pins.leftEncoderX, tFlags.leftEncoder_debug, tFlags.leftEncoder_enabled, "Left")
        ## The right encoder object.
        rightEncoder = AMT103.AMT103(pins.rightEncoderX, tFlags.rightEncoder_debug, tFlags.rightEncoder_enabled, "Right")

        # Start left encoder thread
        if tFlags.leftEncoder_enabled:
            thread_leftenc = threading.Thread(target = leftEncoder.run, args = (globals, ))
            thread_leftenc.start()
        elif tFlags.DriveControl_debug:
            print(debugPrefix + ": left encoder thread is not started")

        # Start right encoder thread
        if tFlags.rightEncoder_enabled:
            thread_rightenc = threading.Thread(target = rightEncoder.run, args = (globals, ))
            thread_rightenc.start()
        elif tFlags.DriveControl_debug:
            print(debugPrefix + ": right encoder thread is not started")

    if debug:
        print(debugPrefix + "[run()]: Drive Control initialized")

    # Main loop controlling the drive system.
    while globals['state'] != 'shutdown':
        if enabled:

            state = globals['driveState']

            # Wheel should not be running.
            if state == 'stop':
                if debug:
                    print(debugPrefix + ": turning off motors")
                if enabled:
                    speed = rightSpeed
                    while speed > 0:
                        speed -= 1
                        leftMotor.engage(speed)
                        rightMotor.engage(speed)
                        time.sleep(0.01)
                    
                    speed = 0
                    leftMotor.engage(speed)
                    rightMotor.engage(speed)
                    relay.disable()

            time.sleep(10)
            print("leftEncoder: " + str(leftEncoder.GetCount()))
            print("rightEncoder: " + str(rightEncoder.GetCount()))

    # Wait for threads to end
    if tFlags.leftEncoder_enabled:
        thread_leftenc.join()
    
    if tFlags.rightEncoder_enabled:
        thread_rightenc.join()

    leftSpeed = 0
    rightSpeed = 0
    if debug:
        print(debugPrefix + ": turning off motors")
    if enabled:
        leftMotor.stop()
        rightMotor.stop()
        relay.disable()

    print(debugPrefix + ": end of module")

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
        distance = int(degrees * DISTANCE_PER_DEGREE)
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
            print(self.debugPrefix + "[enable()]: Turning on the wheel relays")
        if self.enabled:
            self.relay.enable()
    
    ## Disable the motors from receiving power.
    def disable(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[disable()]: Turning off the wheel relays")
        if self.enabled:
            self.relay.disable()

    ## Stops both wheel motors.
    def rapidStop(self):
        self.leftSpeed = 0
        self.rightSpeed = 0
        if self.debug:
            print(self.debugPrefix + "[rapidStop()]: turning off motors")
        if self.enabled:
            self.leftMotor.stop()
            self.rightMotor.stop()
            self.relay.disable()