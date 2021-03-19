import os
import time
import importlib
import threading

# module parameters
NORMAL_DRIVE_SPEED = 50
CAUTION_DRIVE_SPEED = 40
OBJECT_DETECTION_SLOW_DOWN_FACTOR = 1.5 # lower number -> more gradual slowdown
stopDistance = 15 # cm
STOP_DISTANCE = 15 # cm
OBJECT_DETECTION_STOP_DISTANCE = 15
PIVOT_SPEED = 18 # % motor speed
DEGREES_OFF_COURSE = 5 # threshold to determine MowBot is off course
DEGREES_FORCE_PIVOT = 90 # number of degrees off course requiring pivot


def slowDownSpeed(distance):
    # reached stop distance
    if distance < OBJECT_DETECTION_STOP_DISTANCE:
        speed = 0
    else:
        speed = int(OBJECT_DETECTION_SLOW_DOWN_FACTOR * (distance - OBJECT_DETECTION_STOP_DISTANCE))
    if speed > NORMAL_DRIVE_SPEED:
        speed = NORMAL_DRIVE_SPEED
    if speed < 0:
        speed = 0
    return speed

def run(globals):
    
    def avoidObject():
        # check for correct distance
        print("Object Avoidacne")
        #globals['destinationHeading'] = globals['heading']
        lastHeading = globals['heading']
        print("last heading: " + str(lastHeading))
        globals['heading'] = 240
        #if globals['forwardClearnce'] < STOP_DISTANCE:
            # reverse
            #continue
            #while globals['forwardClearance'] != 15:
            #    drive.reverse(-50)
            #drive.stop()
            #drive.turn("left")
        # carry out right pivots
        drive.pivotRight(90)
        # avoid routine
        drive.straight(CAUTION_DRIVE_SPEED)
        time.sleep(1)
        globals['heading'] = 240
        while globals['heading'] > lastHeading + 15 or globals['heading'] < lastHeading - 15:
            print("heading: " + str(globals['heading']))
            if globals['state1'] == 'shutdown':
                drive.rapidStop()
                break
            if globals['forwardClearance'] < STOP_DISTANCE:
                print("-------------no good, collision still there-------------")
            # not clear to turn
            elif not globals['leftTurnClear'] and globals['forwardClearance'] > STOP_DISTANCE:
                drive.straight(CAUTION_DRIVE_SPEED)
                print("turn not clear, drive straight")
            # turn
            else:
                drive.setManualSpeed(CAUTION_DRIVE_SPEED - 10, CAUTION_DRIVE_SPEED + 15)
                print("turning")
        print("------------------------------- we did it ----------------")
        # end object avoidance
        drive.straight(NORMAL_DRIVE_SPEED)
        time.sleep(10)
        globals['state1'] = 'manual'


    def collisionResponse():
        drive.rapidStop()
        # temp for testing
        print(debugPrefix + "[collisionResponse()]: start collision response")
        print(debugPrefix + "[collisionResponse()]: Bumper 1 status = " + str(globals['bumper1Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 2 status = " + str(globals['bumper2Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 3 status = " + str(globals['bumper3Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 4 status = " + str(globals['bumper4Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 5 status = " + str(globals['bumper5Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 6 status = " + str(globals['bumper6Pressed']))
        print(debugPrefix + "[collisionResponse()]: Bumper 7 status = " + str(globals['bumper7Pressed']))
        time.sleep(2)
        #globals['state1'] = 'shutdown'

    

    testNum = globals['testNum']
    
    # load test flags
    import mcs.testFlags as tFlags
    if testNum > 0:
        testFile = "test.routines.test" + str(testNum) + ".testFlags"
        tFlags = importlib.import_module(testFile)

    debug = tFlags.DriveSysControl_debug
    enabled = tFlags.DriveSysControl_enabled
    debugPrefix = "[DriveSysCont]"
    if tFlags.DriveSysControl_over:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"
    if debug:
        print(debugPrefix + ": process spawned")
        print(debugPrefix + ": process id = " + str(os.getpid()))

    # load drive control module
    if tFlags.DriveControl_over:
        testDir = "test.routines.test" + str(testNum) + ".DriveControl"
        DriveControl = importlib.import_module(testDir)
    else:
        import mcs.controllers.DriveControl as DriveControl
    # start drive control thread
    if enabled:
        drive = DriveControl.DriveControl()

    # load remote control module
    if tFlags.RemoteControl_over:
        testDir = "test.routines.test" + str(testNum) + ".RemoteControl"
        RemoteControl = importlib.import_module(testDir)
    else:
        import mcs.controllers.RemoteControl as RemoteControl
    # start remote control thread
    if enabled:
        thread_remoteControl = threading.Thread(target = RemoteControl.run, args = (globals, ))
        thread_remoteControl.start()

    # wait for remote controller to start routine
    # if disabled, program will wait 3 seconds then start
    while globals['state2'] == 'waitForRemote':
        if globals['state1'] == 'manual' or globals['state1'] == 'shutdown':
            break
        time.sleep(1)

    # wait 3 seconds, start driving
    time.sleep(3)
    driveSpeed = NORMAL_DRIVE_SPEED
    drive.enable()
    print("driving forward")
    #drive.straight(driveSpeed)
    drive.pivotRight(360)
    
    compassDrive = False

    # main loop, run until program shutdown
    while globals['state1'] != 'shutdown':

        # check for objects in path (1 meter)
        #forwardClearance = globals['forwardClearance']
        #if forwardClearance < 27:
        #    print("state change, object avoidance--------------")
        #    globals['state1'] = 'objectAvoidance'
        #if forwardClearance > 100:
        #    drive.straight(NORMAL_DRIVE_SPEED)
        #else:
        #    drive.straight(slowDownSpeed(forwardClearance))


        if globals['state1'] == 'objectAvoidance':
            avoidObject()

        # object avoidance clearance debug
        #print("left clearance: " + str(globals['leftTurnClear']))

        # drive based on compass heading
        if compassDrive:
            heading = globals['heading']
            destinationHeading = globals['destinationHeading']
            degreesOff = abs(heading - destinationHeading)
            if heading < destinationHeading:
                veerTo = 'right'
            if heading > destinationHeading:
                veerTo = 'left'
            if degreesOff > 180:
                # veering left
                if 360 - heading + destinationHeading <= 180:
                    degreesOff = 360 - heading + destinationHeading
                    veerTo = 'right'
                # veering right
                elif 360 - destinationHeading + heading >= 180 :
                    degreesOff = 360 - destinationHeading + heading
                    veerTo = 'left'
                else:
                    print("degrees off > 180 problem")
            # no heading available, GPS likely disabled
            if heading == -1 or destinationHeading == -1:
                drive.straight(NORMAL_DRIVE_SPEED)
                print("no data")
            # on course, drive straight
            elif degreesOff <= DEGREES_OFF_COURSE:
                drive.straight(NORMAL_DRIVE_SPEED)
                print("straight")
            # far off course, pivot 
            elif degreesOff >= DEGREES_FORCE_PIVOT:
                # determine pivot direction
                # pivot rigtht or left
                print("way off course")
                # freeze gps heading
            # veering right or left, no pivot required
            elif degreesOff < DEGREES_FORCE_PIVOT and degreesOff > DEGREES_OFF_COURSE:
                # veering left
                if veerTo == 'right':
                    drive.veerRightDegrees(degreesOff)
                    print("veering left")
                else:
                    drive.veerLeftDegrees(degreesOff)
                    print("veering right")
            # invalid state
            else:
            #    continue
                print("Error. Heading: ", heading)
        
        # check if collision has occured
        if globals['state1'] == 'collision':
            collisionResponse()

        # check if manual mode engaged
        if globals['state1'] == 'manual':
            drive.enable()
            while globals['state1'] == 'manual':
                drive.setManualSpeed(globals['leftSpeed'], globals['rightSpeed'])
        
    globals['bladesOn'] = False
    drive.stop()   

    if debug:
        print(debugPrefix + ": end of program")
