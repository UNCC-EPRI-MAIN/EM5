## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file DriveControl.py
# Controls the wheel motors and implements driving and turning.

# standard libraries
import time

import threading
import importlib

# Load Initial Modules
import mcs.PinAssignments as pins

# Firmware modules
import mcs.firmware.RelayControl as RelayControl
import mcs.firmware.Sabertooth2x60 as Sabertooth2x60
import mcs.firmware.AMT103 as AMT103

## Speed of the robot in each phase.
NORMAL_DRIVE_SPEED = 50
PIVOT_SPEED = 18
CAUTION_DRIVE_SPEED = 25

#TODO: Wheel base will be changed. DISTANCE_WHEEL_TO_WHEEL
## Real stats on about the robot.
WHEEL_DIAMETER = 33                                                         # diameter in cm
DISTANCE_WHEEL_TO_WHEEL = 93                                                # distance in cm measured from center of wheel to other
GEAR_RATIO = 26                                                             # 26 motor rotations for one wheel rotation

## Params
OBJECT_DETECTION_SLOW_DOWN_FACTOR = 1.5                                     # lower number -> more gradual slowdown
OBJECT_DETECTION_STOP_DISTANCE = 15                                         # cm
ENCODER_TOLERANCE = 10                                                      # The amount of pulses that the encoder can be out of phase.

## Calculated Values for travel.
PIVOT_CIRCUMFERENCE = 3.14 * DISTANCE_WHEEL_TO_WHEEL
DISTANCE_PER_DEGREE = PIVOT_CIRCUMFERENCE / 360                             
INDEX_PULSE_PER_WHEEL_ROTATION = GEAR_RATIO                                 # index will pulse 26 times per wheel rotation
INDEX_CHANGE_PER_WHEEL_ROTATION = 2 * GEAR_RATIO                            # 26 pulses = 52 state changes on pin
WHEEL_CIRCUMFERENCE = 3.14 * WHEEL_DIAMETER                                 # circumference in cm
DISTANCE_PER_STEP = WHEEL_CIRCUMFERENCE / INDEX_CHANGE_PER_WHEEL_ROTATION   # distance in cm for each step

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
        
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"

    ## The speed of the left wheel.
    leftSpeed = 0
    
    ## The speed of the right wheel.
    rightSpeed = 0

    ## The state of the drive system.
    currentState = 'stop'

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
            ## Auto mode
            if globals['state'] == 'mow':
                newState = globals['driveState']
                if currentState != newState:

                    currentState = newState
                    # Wheel should not be running.
                    if currentState == 'stop':
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
                            if debug:
                                print(debugPrefix + ": Turning off the wheel relays")
                            relay.disable()

                    ## Makes the robot drive straight.
                    elif currentState == 'straight':

                        # Start the wheel relay
                        if enabled and tFlags.wheelRelay_enabled:
                            if relay.GetState():
                                relay.enable()
                            if debug:
                                print(debugPrefix + ": Turning on the wheel relays")

                        # Set the speed of the robot and start driving.
                        leftSpeed = NORMAL_DRIVE_SPEED
                        rightSpeed = NORMAL_DRIVE_SPEED
                        if debug:
                            print(debugPrefix + ": driving straight")
                        if enabled:
                            leftMotor.engage(leftSpeed)
                            rightMotor.engage(rightSpeed)
                        
                        rightEncoder.ResetCount()
                        leftEncoder.ResetCount()

                        leftEncoderCount = 0
                        rightEncoderCount = 0

                        # Drive straight until the system needs to do something else.
                        while globals['driveState'] == 'straight':

                            leftEncoderCount = leftEncoder.GetCount()
                            rightEncoderCount = rightEncoder.GetCount()

                            # if right motor is too fast, speed up the left motor 
                            if((leftEncoderCount + ENCODER_TOLERANCE) < rightEncoderCount):
                                leftSpeed += 1
                                leftMotor.engage(leftSpeed)

                            # if the left motor is too fast.
                            elif ((rightEncoderCount + ENCODER_TOLERANCE) < leftEncoderCount):
                                
                                rightSpeed += 1
                                rightMotor.engage(rightSpeed)

                            # Reset the robot back to the orginal values.
                            else:
                                leftSpeed = NORMAL_DRIVE_SPEED
                                rightSpeed = NORMAL_DRIVE_SPEED

                                leftMotor.engage(leftSpeed)
                                rightMotor.engage(rightSpeed)

                        leftSpeed = 0
                        rightSpeed = 0

                        if debug:
                            print(debugPrefix + ": not driving straight")
                        if enabled:
                            leftMotor.stop()
                            rightMotor.stop()

                    ## Slows the robot down when driving straight.
                    elif currentState == 'cautionstraight':

                        # Start the wheel relay
                        if enabled and tFlags.wheelRelay_enabled:
                            if relay.GetState():
                                relay.enable()
                            if debug:
                                print(debugPrefix + ": Turning on the wheel relays")

                        # Set the speed of the robot and start driving.
                        leftSpeed = CAUTION_DRIVE_SPEED
                        rightSpeed = CAUTION_DRIVE_SPEED
                        if debug:
                            print(debugPrefix + ": driving straight (caution)")
                        if enabled:
                            leftMotor.engage(leftSpeed)
                            rightMotor.engage(rightSpeed)
                        
                        rightEncoder.ResetCount()
                        leftEncoder.ResetCount()

                        leftEncoderCount = 0
                        rightEncoderCount = 0

                        # Drive straight until the system needs to do something else.
                        while globals['driveState'] == 'cautionstraight':

                            leftEncoderCount = leftEncoder.GetCount()
                            rightEncoderCount = rightEncoder.GetCount()

                            # if right motor is too fast, speed up the left motor 
                            if((leftEncoderCount + ENCODER_TOLERANCE) < rightEncoderCount):
                                leftSpeed += 1
                                leftMotor.engage(leftSpeed)

                            # if the left motor is too fast.
                            elif ((rightEncoderCount + ENCODER_TOLERANCE) < leftEncoderCount):
                                
                                rightSpeed += 1
                                rightMotor.engage(rightSpeed)

                            # Reset the robot back to the orginal values.
                            else:
                                leftSpeed = CAUTION_DRIVE_SPEED
                                rightSpeed = CAUTION_DRIVE_SPEED

                                leftMotor.engage(leftSpeed)
                                rightMotor.engage(rightSpeed)

                        leftSpeed = 0
                        rightSpeed = 0

                        if debug:
                            print(debugPrefix + ": not driving straight")
                        if enabled:
                            leftMotor.stop()
                            rightMotor.stop()

                    ## Makes the robot drive straight.
                    elif currentState == 'backward':

                        # Start the wheel relay
                        if enabled and tFlags.wheelRelay_enabled:
                            if relay.GetState():
                                relay.enable()
                            if debug:
                                print(debugPrefix + ": Turning on the wheel relays")

                        # Set the speed of the robot and start driving.
                        leftSpeed = -CAUTION_DRIVE_SPEED
                        rightSpeed = -CAUTION_DRIVE_SPEED
                        if debug:
                            print(debugPrefix + ": driving backward")
                        if enabled:
                            leftMotor.engage(leftSpeed)
                            rightMotor.engage(rightSpeed)
                        
                        rightEncoder.ResetCount()
                        leftEncoder.ResetCount()

                        leftEncoderCount = 0
                        rightEncoderCount = 0

                        # Drive straight until the system needs to do something else.
                        while globals['driveState'] == 'backward':

                            leftEncoderCount = leftEncoder.GetCount()
                            rightEncoderCount = rightEncoder.GetCount()

                            # if right motor is too fast, speed up the left motor 
                            if((leftEncoderCount + ENCODER_TOLERANCE) < rightEncoderCount):
                                leftSpeed -= 1
                                leftMotor.engage(leftSpeed)

                            # if the left motor is too fast.
                            elif ((rightEncoderCount + ENCODER_TOLERANCE) < leftEncoderCount):
                                
                                rightSpeed -= 1
                                rightMotor.engage(rightSpeed)

                            # Reset the robot back to the orginal values.
                            else:
                                leftSpeed = -CAUTION_DRIVE_SPEED
                                rightSpeed = -CAUTION_DRIVE_SPEED

                                leftMotor.engage(leftSpeed)
                                rightMotor.engage(rightSpeed)

                        leftSpeed = 0
                        rightSpeed = 0

                        if debug:
                            print(debugPrefix + ": not driving backward")
                        if enabled:
                            leftMotor.stop(leftSpeed)
                            rightMotor.stop(rightSpeed)
        
                    ## Turn the robot CW
                    elif currentState == 'pivotRight':
                        distance = int(globals['degrees'] * DISTANCE_PER_DEGREE)
                        if debug:
                            print(debugPrefix + ": degrees = " + str(globals['degrees']))
                            print(debugPrefix + ": distance (cm) to travel = " + str(distance))
                        if enabled:
                            
                            pulseCount = int(distance / DISTANCE_PER_STEP)
                            leftSpeed = PIVOT_SPEED
                            rightSpeed = -PIVOT_SPEED
                            leftEncoderCount = 0
                            rightEncoderCount = 0

                            leftMotor.engage(leftSpeed)
                            rightMotor.engage(rightSpeed)
                            
                            while ((leftEncoderCount < pulseCount) or (rightEncoderCount < pulseCount)):
                                
                                leftEncoderCount = leftEncoder.GetCount()
                                rightEncoderCount = rightEncoder.GetCount()
                                
                                if((leftEncoderCount + ENCODER_TOLERANCE) < rightEncoderCount):
                                    leftSpeed += 1
                                    leftMotor.engage(leftSpeed)

                                elif ((rightEncoderCount + ENCODER_TOLERANCE) < leftEncoderCount):
                                    rightSpeed -= 1
                                    rightMotor.engage(rightSpeed)

                                else:

                                    leftSpeed = PIVOT_SPEED
                                    rightSpeed = -PIVOT_SPEED

                                    leftMotor.engage(leftSpeed)
                                    rightMotor.engage(rightSpeed)
                                
                                # Stop motors when they reach the distance.
                                if (leftEncoderCount >= pulseCount):
                                    leftMotor.stop()
                                if (rightEncoderCount >= pulseCount):
                                    rightMotor.stop()

                            leftMotor.stop()
                            rightMotor.stop()
                            if debug:
                                print(debugPrefix + "[pivotRight]: pivot complete")
                            
                            globals['driveState'] = 'completed'

                    ## Turn the robot CCW
                    elif currentState == 'pivotLeft':
                        distance = int(globals['degrees'] * DISTANCE_PER_DEGREE)
                        if debug:
                            print(debugPrefix + ": degrees = " + str(globals['degrees']))
                            print(debugPrefix + ": distance (cm) to travel = " + str(distance))
                        if enabled:
                            pulseCount = int(distance / DISTANCE_PER_STEP)
                            leftSpeed = -PIVOT_SPEED
                            rightSpeed = PIVOT_SPEED
                            leftEncoderCount = 0
                            rightEncoderCount = 0

                            leftMotor.engage(leftSpeed)
                            rightMotor.engage(rightSpeed)
                            
                            while ((leftEncoderCount < pulseCount) or (rightEncoderCount < pulseCount)):
                                
                                leftEncoderCount = leftEncoder.GetCount()
                                rightEncoderCount = rightEncoder.GetCount()
                                
                                if((leftEncoderCount + ENCODER_TOLERANCE) < rightEncoderCount):
                                    leftSpeed -= 1
                                    leftMotor.engage(leftSpeed)

                                elif ((rightEncoderCount + ENCODER_TOLERANCE) < leftEncoderCount):
                                    rightSpeed += 1
                                    rightMotor.engage(rightSpeed)

                                else:

                                    leftSpeed = -PIVOT_SPEED
                                    rightSpeed = PIVOT_SPEED

                                    leftMotor.engage(leftSpeed)
                                    rightMotor.engage(rightSpeed)
                                
                                # Stop motors when they reach the distance.
                                if (leftEncoderCount >= pulseCount):
                                    leftMotor.stop()
                                if (rightEncoderCount >= pulseCount):
                                    rightMotor.stop()

                            leftMotor.stop()
                            rightMotor.stop()
                            if debug:
                                print(debugPrefix + "[pivotLeft]: pivot complete")

                            globals['driveState'] = 'completed'

            # Using the remote controller.
            elif globals['state'] == 'manual':
                if enabled:
                    # Check if the relay is already open.
                    if relay.GetState():
                        relay.enable()
                    # Set the speed according to the remote.
                    leftMotor.engage(globals['leftSpeed'])
                    rightMotor.engage(globals['rightSpeed'])


    # Wait for threads to end
    if tFlags.leftEncoder_enabled:
        thread_leftenc.join()
    
    if tFlags.rightEncoder_enabled:
        thread_rightenc.join()

    # Turn off the wheels
    leftSpeed = 0
    rightSpeed = 0
    if debug:
        print(debugPrefix + ": turning off motors")
    if enabled:
        leftMotor.stop()
        rightMotor.stop()
        if debug:
            print(debugPrefix + ": Turning off the wheel relays")
        relay.disable()

    print(debugPrefix + ": end of module")
        