## @package mcs.controllers
# This software layer interfaces the components and the overall control system.

## @file RemoteControl.py
# Handles the input from the controller.

# standard libraries
import time
import RPi.GPIO as GPIO
import inputs
import importlib

# module parameters
normalDriveSpeed = 60
turnFactor = 15

## Returns the speed based on the angles of the joystick.
def updateSpeed(leftAxis, rightAxis):
    speedPercent = leftAxis / 32768
    baseSpeed = int(normalDriveSpeed * speedPercent)
    turnPercent = rightAxis / 32768
    # forward right
    if turnPercent > 0 and speedPercent > 0.15:
        leftSpeed = baseSpeed + int(turnFactor * turnPercent)
        rightSpeed = baseSpeed - int(turnFactor * turnPercent)
    
    # forward left
    elif turnPercent < 0 and speedPercent >= 0.15:
        leftSpeed = baseSpeed - int(turnFactor * turnPercent * -1)
        rightSpeed = baseSpeed + int(turnFactor * turnPercent * -1)

    # forward
    elif turnPercent < 0.1 and turnPercent > -0.1 and speedPercent >= 0.15:
        leftSpeed = baseSpeed
        rightSpeed = baseSpeed

    # pivot right
    elif turnPercent >= 0.1 and speedPercent > -0.15 and speedPercent < 0.15:
        leftSpeed = 60
        rightSpeed = -60

    # pivot left
    elif turnPercent <= -0.1 and speedPercent > -0.15 and speedPercent < 0.15:
        leftSpeed = -60
        rightSpeed = 60

    # backwards
    elif speedPercent < -0.15:
        leftSpeed = -50
        rightSpeed = -50

    # stopped
    else:
        leftSpeed = 0
        rightSpeed = 0
    
    return leftSpeed, rightSpeed

## The function that the spawned process uses.
def run(globals):

    # load test flags
    tFlags = importlib.import_module(globals['flagFile'])

    ## Boolean indicating if debug info should be included for this module
    debug = tFlags.RemoteControl_debug

    ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
    enabled = tFlags.RemoteControl_enabled

    ## String used for debugging
    debugPrefix = "[RemoteControl]"

    leftSpeed = 0
    prevLeftSpeed = 0
    rightSpeed = 0
    prevRightSpeed = 0
    manualMode = False
    leftAxis = 0
    rightAxis = 0

    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"
    debugPrefix += ": "  
    if debug:
        print(debugPrefix + "starting RemoteControl")

    # main loop, run until end of program
    while globals['state1'] != 'shutdown':
        if enabled:
            
            try:
                # Wait for controller events
                events = inputs.get_gamepad()
                
                for event in events:
                    # yellow button pressed
                    if event.code == 'BTN_WEST' and event.state == 1:
                        # already in manual, resume program
                        # future, shutdown for now
                        if manualMode:
                            if debug:
                                print(debugPrefix + "yellow button pressed, exit manual drive, shutdown")
                            globals['state1'] = 'shutdown'
                            break
                        else:
                            if debug:
                                print(debugPrefix + "yellow button pressed, init manual drive mode")
                            manualMode = True
                            leftSpeed = 0
                            rightSpeed = 0
                            globals['state1'] = 'manual'    
                        
                    # blue button pressed
                    elif event.code == 'BTN_NORTH' and event.state == 1:
                        if debug:
                            print(debugPrefix + "blue button pressed, init shutdown")
                        globals['state1'] = 'shutdown'
                        break

                    # red button pressed
                    elif event.code == 'BTN_EAST' and event.state == 1:
                        if debug:
                            print(debugPrefix + "red button pressed, init clear GPIO")
                        GPIO.cleanup()
                        break

                    # green button pressed
                    elif event.code == 'BTN_SOUTH' and event.state == 1:
                        # start program if in startup
                        if globals['state2'] == 'waitForRemote':   
                            if debug:
                                print(debugPrefix + "starting mow routine")
                            globals['state1'] = 'mow'
                            globals['state2'] = None
                        # else pause program (future)
                        if debug:
                            print(debugPrefix + "green button pressed")

                    # left trigger button pressed
                    elif event.code == 'BTN_TL' and event.state == 1:
                        if debug:
                            print(debugPrefix + "left trigger button pressed, stop blades")
                        globals['bladesOn'] = False

                    # right trigger button pressed
                    elif event.code == 'BTN_TR' and event.state == 1:
                        if debug:
                            print(debugPrefix + "right trugger button pressed, engage blades")
                        globals['bladesOn'] = True

                    # left pad pressed
                    elif event.code == 'ABS_HAT0X' and event.state == -1:
                        if debug:
                            print(debugPrefix + "left pad pressed")
                    
                    # right pad pressed
                    elif event.code == 'ABS_HAT0X' and event.state == 1:
                        if debug:
                            print(debugPrefix + "right pad pressed")

                    # top pad pressed
                    elif event.code == 'ABS_HAT0Y' and event.state == -1:
                        if debug:
                            print(debugPrefix + "top pad pressed")

                    # buttom pad pressed
                    elif event.code == 'ABS_HAT0Y' and event.state == 1:
                        if debug:
                            print(debugPrefix + "bottom pad pressed")

                    # left trigger change position
                    # event.state varies from 0 - 255
                    elif event.code == 'ABS_Z':
                        if debug:
                            print(debugPrefix + "left trigger change of position")

                    # right trigger change position
                    # event.state varies from 0 - 255
                    elif event.code == 'ABS_RZ':
                        if debug:
                            print(debugPrefix + "right trigger change of position")

                    # left joystick pressed
                    # event.state varies from 32767 (down) - -3727 (up)
                    elif event.code == 'ABS_Y':
                        # if in manual, update speed
                        if manualMode:
                            leftAxis = -1 * event.state
                            leftSpeed, rightSpeed = updateSpeed(leftAxis, rightAxis)
                            # update globals if new values
                            if leftSpeed != prevLeftSpeed or rightSpeed != prevRightSpeed:
                                globals['leftSpeed'] = leftSpeed
                                globals['rightSpeed'] = rightSpeed
                                prevLeftSpeed = leftSpeed
                                prevRightSpeed = rightSpeed
                    
                    # right joystick pressed
                    # event.state varies from -32768 (left) - 32767 (right)
                    elif event.code == 'ABS_RX':
                        # if in manual, update speed
                        if manualMode:
                            rightAxis = event.state
                            leftSpeed, rightSpeed = updateSpeed(leftAxis, rightAxis)
                            # update globals if new values
                            if leftSpeed != prevLeftSpeed or rightSpeed != prevRightSpeed:
                                globals['leftSpeed'] = leftSpeed
                                globals['rightSpeed'] = rightSpeed
                                prevLeftSpeed = leftSpeed
                                prevRightSpeed = rightSpeed
            except:
                print("Game controller was not found.")
            
            
            