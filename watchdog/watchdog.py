import time
import RPi.GPIO as GPIO

import inputs

print(inputs.devices.gamepads)

try:
    while True:
        events = inputs.get_gamepad()
        for event in events:
            if event.code == 'BTN_EAST' and event.state == 1:
                print("!! EMERGENCY CUTOFF :: CLEARING GPIO !!")
                GPIO.cleanup()
except:
    print("!! WATCHDOG FAILED :: CLEARING GPIO !!")
    GPIO.cleanup()