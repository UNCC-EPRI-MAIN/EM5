import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module to be tested
from mcs.controllers.BladeControl import BladeControl
#import mcs.TestFlags

print("\n\n<---------- Testbench for Blade Control ---------->\n")


# create relay instance
# relay should be open by default
blades = BladeControl()

#test routine
time.sleep(2)
blades.turnOn()
time.sleep(2)
blades.turnOff()
time.sleep(2)

GPIO.cleanup()
print("\n<---------- Test Complete ---------->\n\n")