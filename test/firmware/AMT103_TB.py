# Modified by Ithamar and Keith

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 

# module to be tested
from mcs.firmware.AMT103 import AMT103

print("\n\n<---------- Testbench for Bumper ---------->\n")


# create bumper instance
# the bumper should be open by default



encRight = AMT103(24, 0, True, True, False, "left")


#test routine
encRight.countDown(1040)     
   
GPIO.cleanup()
