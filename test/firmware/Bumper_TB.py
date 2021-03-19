# Modified by Ithamar and Keith

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module to be tested
from mcs.firmware.Bumper import Bumper

print("\n\n<---------- Testbench for Bumper ---------->\n")


# create bumper instance
# the bumper should be open by default
r1Pin = 25
r1DebugFlag = True
r1EnabledFlag = True
r1DebugName = "relay1"


r1 = Bumper(r1Pin, r1DebugFlag, r1EnabledFlag, True, r1DebugName)


#test routine
while True:
    #Monitor the state of the Bumper
    bumper_state = r1.state()      
   
GPIO.cleanup()
