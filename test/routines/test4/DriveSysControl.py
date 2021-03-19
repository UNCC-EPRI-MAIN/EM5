import os
import time
import importlib
import threading

def run(globals):

    def driveToGPS():
        print("return to base")

    def dockToDoghouse():
        print("docking routine")

    def manualMode():
        globals['state1'] = 'manual'
        leftSpeed = 0
        rightSpeed = 0
        #drive.stop()
        drive.enable()
        drive.manualSetLeftSpeed(leftSpeed)
        drive.manualSetRightSpeed(rightSpeed)
        thread_remoteControlWatchdog = threading.Thread(target = remoteControl.manualDrive)
        thread_remoteControlWatchdog.start()
        while True:
            if remoteControl.interrupt == 'shutdown':
                globals['state1'] = 'shutdown'
                break
            if remoteControl.interrupt == 'exitManual':
                globals['state1'] = 'mow'
                break
            if remoteControl.leftSpeed != leftSpeed:
                leftSpeed = remoteControl.leftSpeed
                drive.manualSetLeftSpeed(leftSpeed)
            if remoteControl.rightSpeed != rightSpeed:
                rightSpeed = remoteControl.rightSpeed
                drive.manualSetRightSpeed(rightSpeed)
        drive.stop()
        drive.disable()
        print("end manual")

    def collision():
        print("collision happened")

    testNum = globals['testNum']
    
    # load test flags
    import mcs.testFlags as tFlags
    if testNum > 0:
        testFile = "test.routines.test" + str(testNum) + ".testFlags"
        tFlags = importlib.import_module(testFile)

    # load drive controller
    if tFlags.DriveControl_over:
        testDir = "test.routines.test" + str(testNum) + ".DriveControl"
        DriveControl = importlib.import_module(testDir)
    else:
        import mcs.controllers.DriveControl as DriveControl

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

    if enabled:
        drive = DriveControl.DriveControl()

    
    import mcs.controllers.RemoteControl as RemoteControl
    remoteControl = RemoteControl.RemoteControl()
    #thread_waitForRemoteStart = threading.Thread(target = RemoteControl.waitToStart)
    #thread_waitForRemoteStart.start()

    def startRemoteControlWatchdog():
        thread_remoteControlWatchdog = threading.Thread(target = remoteControl.watchdog)
        thread_remoteControlWatchdog.start()

    print("this one is not like the others")

    print("waiting to start")
    remoteControl.waitToStart()
    print("start")

    #drive.straight(50)
    #time.sleep(60)
    #drive.stop()   

    startRemoteControlWatchdog()
    
    

    while globals['state1'] != 'shutdown':
        if remoteControl.interrupt == 'shutdown':
            globals['state1'] = 'shutdown'
            print("exiting drive system control loop")
            break
        if remoteControl.interrupt == 'manual':
            manualMode()
            if globals['state1'] != 'shutdown':
                startRemoteControlWatchdog()
        if remoteControl.interrupt == 'pause':
            globals['state1'] = 'pause'
            print("pausing")
            
        # check if exit sequence initiated by remote controller
        #globals['exitFromRemoteController'] = RemoteControl.exitProgram
        # check if collision has occured
        #if globals['systemState'] == '':
        #    collision()
        # check charging routine needs to be active
        #print("dong stuff")   
    
    if debug:
        print(debugPrefix + ": end of function")
