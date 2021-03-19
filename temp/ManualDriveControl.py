import signal

from xbox360controller import Xbox360Controller as F710controller

def startProgram(button):
    print("A: start program")

def setStartingPoint(button):
    print("X: set home point")

def killProgram(button):
    print("B: kill program")
    global killProgram
    killProgram = True

def toggleManualDrive(button):
    print("Y: toggle manual")

def controller():
    global killProgram
    try:
        with F710controller(0, axis_threshold=0.2) as controller:
            controller.button_a.when_pressed = startProgram
            controller.button_b.when_pressed = killProgram
            controller.button_x.when_pressed = setStartingPoint
            controller.button_y.when_pressed = toggleManualDrive
            signal.pause()
    except KeyboardInterrupt:
        pass


