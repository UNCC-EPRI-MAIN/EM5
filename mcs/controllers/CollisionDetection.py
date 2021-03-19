import mcs.firmware.Bumper as Bumper
import time
# mcs modules
import mcs.pinAssignments as pins
import mcs.testFlags as tFlags

def run(globals):
    debug = tFlags.CollisionDetection_debug
    ## Boolean to indicate if this motor should be used. If disabled, program will run but not attempt to operate motors.
    enabled = tFlags.CollisionDetection_enabled
    ## String used for debugging
    debugPrefix = "[CollisionDetection]"
    if tFlags.CollisionDetection_over:
        debugPrefix += "[O]"
    if enabled:
        debugPrefix += "[E]"
    else:
        debugPrefix += "[D]"  
    if debug:
        print(debugPrefix + "[run()]: Collision Detection initialized")
    activeCollision = False
    bumper1Pressed = False
    bumper2Pressed = False
    bumper3Pressed = False
    bumper4Pressed = False
    bumper5Pressed = False
    bumper6Pressed = False
    bumper7Pressed = False
    reading = False
    if enabled:
        bumper1 = Bumper.Bumper(pins.bumper1, tFlags.bumper1_debug, tFlags.bumper1_enabled, tFlags.bumper1_over, "Bumper1")
        bumper2 = Bumper.Bumper(pins.bumper2, tFlags.bumper2_debug, tFlags.bumper2_enabled, tFlags.bumper2_over, "Bumper2")
        bumper3 = Bumper.Bumper(pins.bumper3, tFlags.bumper3_debug, tFlags.bumper3_enabled, tFlags.bumper3_over, "Bumper3")
        bumper4 = Bumper.Bumper(pins.bumper4, tFlags.bumper4_debug, tFlags.bumper4_enabled, tFlags.bumper4_over, "Bumper4")
        bumper5 = Bumper.Bumper(pins.bumper5, tFlags.bumper5_debug, tFlags.bumper5_enabled, tFlags.bumper5_over, "Bumper5")
        bumper6 = Bumper.Bumper(pins.bumper6, tFlags.bumper6_debug, tFlags.bumper6_enabled, tFlags.bumper6_over, "Bumper6")
        bumper7 = Bumper.Bumper(pins.bumper7, tFlags.bumper7_debug, tFlags.bumper7_enabled, tFlags.bumper7_over, "Bumper7")

    while globals['state1'] != 'shutdown':
        if enabled:
            # determine number of bumpers pressed        
            bumpersPressed = 0

            # get bumper 1 reading
            if bumper1.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper1Pressed:
                bumper1Pressed = reading
                globals['bumper1Pressed'] = reading

            # get bumper 2 reading
            if bumper2.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper2Pressed:
                bumper2Pressed = reading
                globals['bumper2Pressed'] = reading
            
            # get bumper 3 reading
            if bumper3.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper3Pressed:
                bumper3Pressed = reading
                globals['bumper3Pressed'] = reading
            
            # get bumper 4 reading
            if bumper4.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper4Pressed:
                bumper4Pressed = reading
                globals['bumper4Pressed'] = reading
            
            # get bumper 5 reading
            if bumper5.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper5Pressed:
                bumper5Pressed = reading
                globals['bumper5Pressed'] = reading
            
            # get bumper 6 reading
            if bumper6.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper6Pressed:
                bumper6Pressed = reading
                globals['bumper6Pressed'] = reading
            
            # get bumper 7 reading
            if bumper7.state() == 0:
                bumpersPressed = bumpersPressed + 1
                reading = True
            else:
                reading = False
            # check if global update needed
            if reading != bumper7Pressed:
                bumper7Pressed = reading
                globals['bumper7Pressed'] = reading

            # new collision detected
            if bumpersPressed > 0 and not activeCollision:
                activeCollision = True
                globals['state1'] = 'collision'
                globals['state2'] = 'detection'
                if debug:
                    print(debugPrefix + ": collision detected")
            
            # collision ended
            if bumpersPressed == 0 and activeCollision:
                activeCollision = False
                if debug:
                    print(debugPrefix + ": collision over")

            if debug:
                print(debugPrefix + ": active bumpers = " + str(bumpersPressed))
    print(debugPrefix + "end of module")
                