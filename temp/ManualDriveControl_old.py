import signal
from xbox360controller import Xbox360Controller
import mcs.TestFlags as flags



#from mcs.TestFlags import TestFlags
class ManualDriveControl:

    def __init__(self):
        self.debug = flags.ManualDriveControl_debug
        self.enabled = flags.ManualDriveControl_enabled
        self.debugPrefix = "[ManualDriveControl]"
        #self.speed = 0
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.leftAxis = 0
        self.manualEngaged = False
        self.rightAxis = 0
        self.MAXSPEED = 50
        self.TURNFACTOR = 10
        self.exitManualDrive = False
        if self.enabled:
            self.debugPrefix += "[E]"
        else:
            self.debugPrefix += "[D]"  
        if self.debug:
            print(self.debugPrefix + "[__init__()]: defining manual drive control")
        if self.enabled:
            self.waitForEvent()

    def pauseForProgramStart():
        print("program start")

    def waitForEvent(self):
        self.manualEngaged = False
        try:
            with Xbox360Controller(0, axis_threshold=0.2) as controller:
                            # Button b events
                controller.button_b.when_pressed = self.buttonBPressed
                            # Button y events
                controller.button_y.when_pressed = self.toggleManualDrive
                signal.pause()
        except KeyboardInterrupt:
            pass

    def buttonAPressed(self, button):
        print("a")

    def buttonBPressed(self, button):
        print("b")

    def toggleManualDrive(self, button):
        print("y")
        if self.manualEngaged == False:
            print("manual engage")
            self.engageManualDrive()
        else:
            self.waitForEvent()

    def buttonXPressed(self, button):
        print("x")

    def leftAxisMoved(self, axis):
        self.leftAxis = -axis.y
        if abs(self.leftAxis) < 0.25:
            self.leftAxis = 0
        if abs(self.rightAxis) < 0.25:
            self.rightAxis = 0
        self.updateSpeed()

    def rightAxisMoved(self, axis):
        self.rightAxis = axis.x
        if abs(self.leftAxis) < 0.25:
            self.leftAxis = 0
        if abs(self.rightAxis) < 0.25:
            self.rightAxis = 0
        self.updateSpeed()

    def engageManualDrive(self):
        self.manualEngaged = True
        try:
            with Xbox360Controller(0, axis_threshold=0.2) as controller:
                controller.button_y.when_pressed = self.toggleManualDrive
                controller.axis_l.when_moved = self.leftAxisMoved
                controller.axis_r.when_moved = self.rightAxisMoved
                signal.pause()
        except KeyboardInterrupt:
            pass

    def updateSpeed(self):
        # drive forward
        if self.leftAxis > 0:
            self.leftSpeed = int(self.MAXSPEED * self.leftAxis)
            self.rightSpeed = int(self.MAXSPEED * self.leftAxis)
            if self.rightAxis > 0:
                self.rightSpeed -= int(self.TURNFACTOR * self.rightAxis)
            else:
                self.leftSpeed -= int(self.TURNFACTOR * self.rightAxis)
        # drive backwards
        elif self.leftAxis < 0:
            print("drive backwards")
        # pivot right
        elif self.rightAxis > 0:
            print("hard right")
        #pivot left
        elif self.rightAxis < 0:
            print("hard left")
        # else stop
        else:
            self.leftSpeed = 0
            self.rightSpeed = 0
        print(str(self.leftSpeed) + " " + str(self.rightSpeed))
